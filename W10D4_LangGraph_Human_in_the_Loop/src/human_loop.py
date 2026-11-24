from typing import TypedDict
from langgraph.graph import StateGraph, START, END
from langgraph.types import interrupt
from langgraph.checkpoint.memory import InMemorySaver


class AgentState(TypedDict, total=False):
    user_input: str
    category: str
    human_decision: str
    response: str
    status: str


def classify_node(state: AgentState):
    """Classify the user's input into one of five categories."""

    message = state["user_input"].lower()

    if any(word in message for word in ["hack", "attack", "steal", "harm"]):
        category = "unsafe"
    elif any(word in message for word in ["hello", "hi", "hey"]):
        category = "greeting"
    elif any(word in message for word in ["calculate", "plus", "add", "multiply"]):
        category = "calculation"
    elif any(word in message for word in ["python", "code", "program", "debug"]):
        category = "coding"
    else:
        category = "question"

    print(f"[CLASSIFY] Category: {category}")

    return {
        "category": category,
        "status": "classified"
    }


def route_node(state: AgentState):
    """Pause execution and request a human decision."""

    decision = interrupt({
        "message": "Human approval required.",
        "user_input": state["user_input"],
        "category": state["category"],
        "options": ["approve", "reject"]
    })

    decision = str(decision).strip().lower()

    print(f"[ROUTE] Human decision: {decision}")

    return {
        "human_decision": decision,
        "status": "reviewed"
    }


def conditional_router(state: AgentState):
    """Choose the next step using classification and human approval."""

    if state.get("category") == "unsafe":
        return "end"

    if state.get("human_decision") == "approve":
        return "respond"

    return "end"


def respond_node(state: AgentState):
    """Generate a simple response after approval."""

    category = state["category"]

    responses = {
        "greeting": "Hello! How can I help you today?",
        "calculation": "Your calculation request has been approved. Please provide the numbers.",
        "coding": "Your coding request has been approved. I can help with Python and programming.",
        "question": "Your question has been approved. Please provide more details."
    }

    response = responses.get(
        category,
        "The request cannot be processed."
    )

    print("[RESPOND] Generating response...")

    return {
        "response": response,
        "status": "completed"
    }


def build_graph():
    """Build and compile the three-node LangGraph."""

    graph = StateGraph(AgentState)

    graph.add_node("classify", classify_node)
    graph.add_node("route", route_node)
    graph.add_node("respond", respond_node)

    graph.add_edge(START, "classify")
    graph.add_edge("classify", "route")

    graph.add_conditional_edges(
        "route",
        conditional_router,
        {
            "respond": "respond",
            "end": END
        }
    )

    graph.add_edge("respond", END)

    checkpointer = InMemorySaver()

    return graph.compile(checkpointer=checkpointer)