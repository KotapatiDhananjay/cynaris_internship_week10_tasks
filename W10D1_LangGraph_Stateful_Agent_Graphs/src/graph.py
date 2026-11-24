from typing import TypedDict
from langgraph.graph import StateGraph, START, END
from langgraph.checkpoint.memory import InMemorySaver
from langgraph.types import interrupt


class AgentState(TypedDict, total=False):
    user_input: str
    category: str
    human_decision: str
    response: str
    status: str


def classify_node(state: AgentState):
    """Classify the incoming user message."""

    message = state["user_input"].lower()

    unsafe_words = [
        "hack someone's account",
        "steal password",
        "make a bomb",
        "malware",
        "steal credentials",
    ]

    if any(word in message for word in unsafe_words):
        category = "unsafe"
    elif any(word in message for word in ["hello", "hi", "hey", "good morning"]):
        category = "greeting"
    elif any(word in message for word in ["calculate", "add", "multiply", "sum"]):
        category = "calculation"
    elif any(word in message for word in ["python", "code", "program", "debug"]):
        category = "coding"
    else:
        category = "question"

    print(f"[CLASSIFY] Category: {category}")

    return {
        "category": category,
        "status": "classified",
    }


def route_node(state: AgentState):
    """Pause execution and request human approval."""

    category = state["category"]

    human_decision = interrupt({
        "message": "Human review required. Approve or reject this request.",
        "user_input": state["user_input"],
        "category": category,
        "options": ["approve", "reject"],
    })

    decision = str(human_decision).strip().lower()

    print(f"[ROUTE] Human decision: {decision}")

    return {
        "human_decision": decision,
        "status": "reviewed",
    }


def decide_next(state: AgentState):
    """Choose the next step using classification and human input."""

    if state["category"] == "unsafe":
        return "end"

    if state.get("human_decision") == "approve":
        return "respond"

    return "end"


def respond_node(state: AgentState):
    """Generate a response based on the classified category."""

    category = state["category"]
    user_input = state["user_input"]

    if category == "greeting":
        response = "Hello! Welcome to the LangGraph Stateful Agent."
    elif category == "calculation":
        response = (
            "This request has been classified as a calculation task. "
            "It can be sent to a calculator tool for execution."
        )
    elif category == "coding":
        response = (
            "This request has been classified as a coding task. "
            "Please provide the code or programming problem for assistance."
        )
    else:
        response = (
            f"Your question has been approved: {user_input}. "
            "The request is ready for further processing."
        )

    print("[RESPOND] Response generated.")

    return {
        "response": response,
        "status": "completed",
    }


def build_graph():
    """Build and compile the three-node stateful graph."""

    builder = StateGraph(AgentState)

    builder.add_node("classify", classify_node)
    builder.add_node("route", route_node)
    builder.add_node("respond", respond_node)

    builder.add_edge(START, "classify")
    builder.add_edge("classify", "route")

    builder.add_conditional_edges(
        "route",
        decide_next,
        {
            "respond": "respond",
            "end": END,
        },
    )

    builder.add_edge("respond", END)

    memory = InMemorySaver()

    return builder.compile(checkpointer=memory)


# Shared graph instance
graph = build_graph()