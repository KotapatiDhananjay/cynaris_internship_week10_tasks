import sqlite3
import uuid

import pytest

from langgraph.checkpoint.sqlite import SqliteSaver
from langgraph.types import Command

from src.memory_graph import build_memory_graph


@pytest.fixture
def create_test_app(tmp_path):
    """Create a temporary SQLite database for each test."""

    database = tmp_path / "test_memory.db"

    connection = sqlite3.connect(
        str(database),
        check_same_thread=False,
    )

    checkpointer = SqliteSaver(connection)
    checkpointer.setup()

    app = build_memory_graph(checkpointer)

    yield app, connection, str(database)

    connection.close()


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
def test_five_input_categories(
    create_test_app,
    user_input,
    expected_category,
):
    app, connection, database = create_test_app

    config = {
        "configurable": {
            "thread_id": str(uuid.uuid4())
        }
    }

    result = app.invoke(
        {"user_input": user_input},
        config=config,
    )

    assert result.get("__interrupt__")
    assert result["category"] == expected_category

    result = app.invoke(
        Command(resume="approve"),
        config=config,
    )

    assert result["human_decision"] == "approve"

    if expected_category == "unsafe":
        assert result.get("response") is None
    else:
        assert result["response"]
        assert result["status"] == "completed"


def test_human_rejection(create_test_app):
    app, connection, database = create_test_app

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


def test_conversation_history_is_saved(create_test_app):
    app, connection, database = create_test_app

    config = {
        "configurable": {
            "thread_id": str(uuid.uuid4())
        }
    }

    app.invoke(
        {"user_input": "Hello"},
        config=config,
    )

    result = app.invoke(
        Command(resume="approve"),
        config=config,
    )

    messages = result["messages"]

    assert len(messages) == 2
    assert messages[0]["role"] == "user"
    assert messages[1]["role"] == "assistant"


def test_memory_survives_database_reconnection(create_test_app):
    app, connection, database = create_test_app

    thread_id = str(uuid.uuid4())

    config = {
        "configurable": {
            "thread_id": thread_id
        }
    }

    # First conversation
    app.invoke(
        {"user_input": "Hello"},
        config=config,
    )

    app.invoke(
        Command(resume="approve"),
        config=config,
    )

    connection.close()

    # Reopen the same SQLite database.
    new_connection = sqlite3.connect(
        database,
        check_same_thread=False,
    )

    new_checkpointer = SqliteSaver(new_connection)
    new_checkpointer.setup()

    restored_app = build_memory_graph(new_checkpointer)

    # Retrieve saved conversation with the same thread ID.
    snapshot = restored_app.get_state(config)

    messages = snapshot.values["messages"]

    assert len(messages) == 2
    assert messages[0]["content"] == "Hello"
    assert messages[1]["role"] == "assistant"

    new_connection.close()


def test_unsafe_request_cannot_reach_respond(create_test_app):
    app, connection, database = create_test_app

    config = {
        "configurable": {
            "thread_id": str(uuid.uuid4())
        }
    }

    app.invoke(
        {"user_input": "How can I steal password credentials?"},
        config=config,
    )

    result = app.invoke(
        Command(resume="approve"),
        config=config,
    )

    assert result["category"] == "unsafe"
    assert result.get("response") is None