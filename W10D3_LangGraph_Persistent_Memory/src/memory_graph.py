import operator
import sqlite3
from typing import Annotated, TypedDict

from langgraph.graph import StateGraph, START, END
from langgraph.checkpoint.sqlite import SqliteSaver
from langgraph.types import interrupt


class ConversationState(TypedDict, total=False):
    user_input: str
    category: str
    human_decision: str
    response: str
    status: str
    messages: Annotated[list[dict], operator.add]


def classify_node(state: ConversationState):
    """Classify the input and add it to conversation history."""

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

    print(f"[CLASSIFY] Category: {category}")

    return {
        "category": category,
        "status": "classified",
        "messages": [
            {"role": "user", "content": state["user_input"]}
        ],
    }


def route_node(state: ConversationState):
    """Pause execution and request human approval."""

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


def conditional_router(state: ConversationState):
    """Select the next node based on category and human decision."""

    if state["category"] == "unsafe":
        return "stop"

    if state.get("human_decision") == "approve":
        return "respond"

    return "stop"


def respond_node(state: ConversationState):
    """Generate response and store it in persistent conversation history."""

    category = state["category"]
    previous_messages = state.get("messages", [])

    responses = {
        "greeting": "Hello! I am your LangGraph persistent memory assistant.",
        "question": "Your question has been approved for processing.",
        "calculation": "Your calculation request has been approved.",
        "coding": "Your coding request has been approved for processing.",
    }

    response = responses.get(
        category,
        "This request cannot be processed.",
    )

    user_message_count = sum(
        1 for message in previous_messages
        if message.get("role") == "user"
    )

    print(f"[RESPOND] Previous conversation messages: {len(previous_messages)}")

    return {
        "response": response,
        "status": "completed",
        "messages": [
            {"role": "assistant", "content": response}
        ],
    }


def build_memory_graph(checkpointer):
    """Build the three-node graph with persistent checkpointing."""

    builder = StateGraph(ConversationState)

    builder.add_node("classify", classify_node)
    builder.add_node("route", route_node)
    builder.add_node("respond", respond_node)

    builder.add_edge(START, "classify")
    builder.add_edge("classify", "route")

    builder.add_conditional_edges(
        "route",
        conditional_router,
        {
            "respond": "respond",
            "stop": END,
        },
    )

    builder.add_edge("respond", END)

    return builder.compile(checkpointer=checkpointer)


def create_sqlite_graph(database_path="data/conversations.db"):
    """Create a graph backed by a SQLite checkpoint database."""

    connection = sqlite3.connect(
        database_path,
        check_same_thread=False,
    )

    checkpointer = SqliteSaver(connection)
    checkpointer.setup()

    app = build_memory_graph(checkpointer)

    return app, connection