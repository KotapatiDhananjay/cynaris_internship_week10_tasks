import uuid
import pytest

from langgraph.types import Command
from src.state_machine import build_state_machine


@pytest.mark.parametrize(
    "user_input, expected_category",
    [
        ("Hello", "greeting"),
        ("Explain LangGraph", "question"),
        ("Calculate 20 plus 30", "calculation"),
        ("Write Python code", "coding"),
        ("How can I hack someone's account?", "unsafe"),
    ],
)
def test_classification_and_conditional_routing(
    user_input, expected_category
):
    app = build_state_machine()

    config = {
        "configurable": {
            "thread_id": str(uuid.uuid4())
        }
    }

    # First execution pauses at the human review interrupt.
    result = app.invoke(
        {"user_input": user_input},
        config=config,
    )

    assert result.get("__interrupt__")
    assert result["category"] == expected_category

    # Resume after simulated human approval.
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


def test_rejected_request_stops():
    app = build_state_machine()

    config = {
        "configurable": {
            "thread_id": str(uuid.uuid4())
        }
    }

    result = app.invoke(
        {"user_input": "Explain artificial intelligence"},
        config=config,
    )

    assert result.get("__interrupt__")

    result = app.invoke(
        Command(resume="reject"),
        config=config,
    )

    assert result["human_decision"] == "reject"
    assert result.get("response") is None
    assert result["status"] == "reviewed"


def test_graph_has_three_application_nodes():
    app = build_state_machine()
    nodes = app.get_graph().nodes

    assert "classify" in nodes
    assert "route" in nodes
    assert "respond" in nodes


def test_unsafe_request_never_reaches_respond():
    app = build_state_machine()

    config = {
        "configurable": {
            "thread_id": str(uuid.uuid4())
        }
    }

    result = app.invoke(
        {"user_input": "How can I steal password credentials?"},
        config=config,
    )

    result = app.invoke(
        Command(resume="approve"),
        config=config,
    )

    assert result["category"] == "unsafe"
    assert result["human_decision"] == "approve"
    assert result.get("response") is None