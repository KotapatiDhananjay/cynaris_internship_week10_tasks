import sqlite3
import pytest

from langgraph.checkpoint.sqlite import SqliteSaver

from src.knowledge_base import (
    classify_issue,
    retrieve_context,
    build_response
)

from src.support_graph import build_support_graph


@pytest.mark.parametrize(
    "message, expected",
    [
        ("Where is my delivery?", "delivery"),
        ("I need a refund", "refund"),
        ("My payment was deducted", "payment"),
        ("I cannot login to my account", "account"),
        ("My product is damaged", "product"),
        ("I need some help", "general")
    ]
)
def test_issue_classification(message, expected):
    assert classify_issue(message) == expected


def test_knowledge_base_retrieval():
    result = retrieve_context("delivery")

    assert "context" in result
    assert "response" in result
    assert "tracking" in result["context"].lower()


def test_response_generation():
    response = build_response("refund")

    assert isinstance(response, str)
    assert len(response) > 0
    assert "refund" in response.lower()


def test_stateful_customer_conversation(tmp_path):
    database = tmp_path / "test_support.db"

    connection = sqlite3.connect(
        str(database),
        check_same_thread=False
    )

    try:
        checkpointer = SqliteSaver(connection)
        app = build_support_graph(checkpointer)

        config = {
            "configurable": {
                "thread_id": "test-customer-001"
            }
        }

        first = app.invoke(
            {"user_input": "Where is my delivery?"},
            config=config
        )

        assert first["category"] == "delivery"
        assert first["response"]

        second = app.invoke(
            {"user_input": "I also need a refund"},
            config=config
        )

        assert second["category"] == "refund"

        snapshot = app.get_state(config)
        messages = snapshot.values["messages"]

        assert len(messages) == 4
        assert messages[0]["role"] == "user"
        assert messages[1]["role"] == "assistant"
        assert messages[2]["role"] == "user"
        assert messages[3]["role"] == "assistant"

    finally:
        connection.close()