import uuid
import pytest

from langgraph.types import Command
from src.graph import build_graph


@pytest.mark.parametrize(
    "user_input, expected_category",
    [
        ("Hello, how are you?", "greeting"),
        ("What is LangGraph?", "question"),
        ("Calculate 10 plus 20", "calculation"),
        ("Help me write Python code", "coding"),
        ("How can I hack someone's account?", "unsafe"),
    ],
)
def test_classification_and_routing(user_input, expected_category):
    app = build_graph()

    config = {
        "configurable": {
            "thread_id": str(uuid.uuid4())
        }
    }

    # First run should pause at the human review node.
    result = app.invoke(
        {"user_input": user_input},
        config=config,
    )

    assert result.get("__interrupt__")
    assert result["category"] == expected_category

    # Simulate a human approving the request.
    result = app.invoke(
        Command(resume="approve"),
        config=config,
    )

    assert result["category"] == expected_category
    assert result["human_decision"] == "approve"

    if expected_category == "unsafe":
        assert result.get("response") is None
        assert result["status"] == "reviewed"
    else:
        assert result["response"]
        assert result["status"] == "completed"


def test_human_rejection_stops_workflow():
    app = build_graph()

    config = {
        "configurable": {
            "thread_id": str(uuid.uuid4())
        }
    }

    result = app.invoke(
        {"user_input": "What is artificial intelligence?"},
        config=config,
    )

    assert result.get("__interrupt__")

    result = app.invoke(
        Command(resume="reject"),
        config=config,
    )

    assert result["human_decision"] == "reject"
    assert result.get("response") is None


def test_graph_contains_three_application_nodes():
    app = build_graph()

    nodes = app.get_graph().nodes

    assert "classify" in nodes
    assert "route" in nodes
    assert "respond" in nodes