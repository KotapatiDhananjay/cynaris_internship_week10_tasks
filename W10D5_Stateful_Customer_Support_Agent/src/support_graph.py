import operator
from typing import TypedDict, Annotated

from langgraph.graph import StateGraph, START, END

from src.knowledge_base import (
    classify_issue,
    retrieve_context,
    build_response
)

from src.crew import run_support_crew


class SupportState(TypedDict, total=False):
    """State shared between LangGraph nodes."""

    user_input: str
    category: str
    context: str
    response: str
    crew_notes: str
    messages: Annotated[list[dict], operator.add]


def classify_node(state: SupportState):
    """Identify the customer's issue category."""

    message = state["user_input"]
    category = classify_issue(message)

    return {
        "category": category,
        "messages": [
            {"role": "user", "content": message}
        ]
    }


def retrieve_node(state: SupportState):
    """Retrieve relevant support policy."""

    knowledge = retrieve_context(state["category"])

    return {
        "context": knowledge["context"]
    }


def respond_node(state: SupportState):
    """Run the CrewAI team and prepare the customer response."""

    crew_notes = run_support_crew(
        user_input=state["user_input"],
        category=state["category"],
        context=state["context"]
    )

    response = build_response(state["category"])

    return {
        "crew_notes": crew_notes,
        "response": response,
        "messages": [
            {"role": "assistant", "content": response}
        ]
    }


def build_support_graph(checkpointer):
    """Build a persistent three-node customer support graph."""

    graph = StateGraph(SupportState)

    graph.add_node("classify", classify_node)
    graph.add_node("retrieve", retrieve_node)
    graph.add_node("respond", respond_node)

    graph.add_edge(START, "classify")
    graph.add_edge("classify", "retrieve")
    graph.add_edge("retrieve", "respond")
    graph.add_edge("respond", END)

    return graph.compile(checkpointer=checkpointer)