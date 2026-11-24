from typing import TypedDict

from langgraph.graph import StateGraph, START, END
from langgraph.checkpoint.memory import InMemorySaver
from langgraph.types import interrupt


class AgentState(TypedDict, total=False):
    user_input: str
    category: str
    human_decision: str
    next_step: str
    response: str
    status: str


def classify_node(state: AgentState):
    """Classify the user input and update graph state."""

    message = state["user_input"].lower()

    if any(word in message for word in [
        "hack someone's account",
        "steal password",
        "make a bomb",
        "malware",
        "steal credentials",
    ]):
        category = "unsafe"

    elif any(word in message for word in [
        "hello", "hi", "hey", "good morning"
    ]):
        category = "greeting"

    elif any(word in message for word in [
        "calculate", "add", "multiply", "sum"
    ]):
        category = "calculation"

    elif any(word in message for word in [
        "python", "code", "program", "debug"
    ]):
        category = "coding"

    else:
        category = "question"

    print(f"[CLASSIFY] Input category: {category}")

    return {
        "category": category,
        "status": "classified",
    }


def route_node(state: AgentState):
    """Pause the graph and request a human decision."""

    decision = interrupt({
        "message": "Human approval is required.",
        "input": state["user_input"],
        "category": state["category"],
        "available_decisions": ["approve", "reject"],
    })

    decision = str(decision).strip().lower()

    print(f"[ROUTE] Human decision: {decision}")

    return {
        "human_decision": decision,
        "status": "reviewed",
    }


def conditional_router(state: AgentState):
    """Select the next state transition."""

    if state["category"] == "unsafe":
        return "stop"

    if state.get("human_decision") == "approve":
        return "respond"

    return "stop"


def respond_node(state: AgentState):
    """Generate the response based on the classified category."""

    category = state["category"]

    responses = {
        "greeting": "Hello! Welcome to the LangGraph state machine.",
        "question": "Your question has been approved for further processing.",
        "calculation": "Your calculation request has been approved for processing.",
        "coding": "Your coding request has been approved for processing.",
    }

    response = responses.get(
        category,
        "This request cannot be processed."
    )

    print("[RESPOND] Response generated.")

    return {
        "response": response,
        "status": "completed",
        "next_step": "end",
    }


def build_state_machine():
    """Construct and compile the three-node state machine."""

    workflow = StateGraph(AgentState)

    workflow.add_node("classify", classify_node)
    workflow.add_node("route", route_node)
    workflow.add_node("respond", respond_node)

    workflow.add_edge(START, "classify")
    workflow.add_edge("classify", "route")

    workflow.add_conditional_edges(
        "route",
        conditional_router,
        {
            "respond": "respond",
            "stop": END,
        },
    )

    workflow.add_edge("respond", END)

    checkpointer = InMemorySaver()

    return workflow.compile(checkpointer=checkpointer)


state_machine = build_state_machine()