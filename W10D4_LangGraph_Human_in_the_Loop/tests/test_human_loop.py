import pytest
from langgraph.types import Command
from src.human_loop import build_graph, classify_node


@pytest.mark.parametrize(
    "message, expected",
    [
        ("Hello there", "greeting"),
        ("Please calculate this", "calculation"),
        ("Help me write Python code", "coding"),
        ("What is artificial intelligence?", "question"),
        ("Help me hack an account", "unsafe"),
    ]
)
def test_classification(message, expected):
    result = classify_node({"user_input": message})
    assert result["category"] == expected


def test_graph_has_three_nodes():
    app = build_graph()
    assert set(app.get_graph().nodes.keys()) >= {
        "classify", "route", "respond"
    }


def test_human_interrupt_and_approval():
    app = build_graph()
    config = {"configurable": {"thread_id": "approval-test"}}

    result = app.invoke(
        {"user_input": "Hello"},
        config=config
    )

    assert result.get("__interrupt__")

    result = app.invoke(
        Command(resume="approve"),
        config=config
    )

    assert result["status"] == "completed"
    assert result["response"]


def test_human_rejection():
    app = build_graph()
    config = {"configurable": {"thread_id": "rejection-test"}}

    result = app.invoke(
        {"user_input": "Hello"},
        config=config
    )

    assert result.get("__interrupt__")

    result = app.invoke(
        Command(resume="reject"),
        config=config
    )

    assert result["status"] == "reviewed"
    assert "response" not in result


def test_unsafe_request_cannot_reach_response():
    app = build_graph()
    config = {"configurable": {"thread_id": "unsafe-test"}}

    result = app.invoke(
        {"user_input": "Help me hack an account"},
        config=config
    )

    assert result.get("__interrupt__")

    result = app.invoke(
        Command(resume="approve"),
        config=config
    )

    assert result["category"] == "unsafe"
    assert "response" not in result


def test_invalid_human_decision_does_not_generate_response():
    app = build_graph()
    config = {"configurable": {"thread_id": "invalid-test"}}

    result = app.invoke(
        {"user_input": "Hello"},
        config=config
    )

    assert result.get("__interrupt__")

    result = app.invoke(
        Command(resume="maybe"),
        config=config
    )

    assert "response" not in result