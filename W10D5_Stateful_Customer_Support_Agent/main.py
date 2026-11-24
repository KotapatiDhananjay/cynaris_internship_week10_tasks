import sqlite3
from pathlib import Path

from langgraph.checkpoint.sqlite import SqliteSaver

from src.support_graph import build_support_graph
from src.monitoring import log_support_run


def display_history(app, config):
    """Display saved messages for the current customer."""

    print("\n========== CUSTOMER HISTORY ==========")

    try:
        snapshot = app.get_state(config)
        messages = snapshot.values.get("messages", [])
    except Exception:
        messages = []

    if not messages:
        print("No previous conversation found.")
        return

    for message in messages:
        role = message.get("role", "unknown").upper()
        print(f"{role}: {message.get('content', '')}")


def main():
    Path("data").mkdir(exist_ok=True)

    connection = sqlite3.connect(
        "data/customer_support.db",
        check_same_thread=False
    )

    checkpointer = SqliteSaver(connection)
    checkpointer.setup()

    app = build_support_graph(checkpointer)

    print("\n============================================")
    print(" STATEFUL CUSTOMER SUPPORT AGENT")
    print("============================================")

    thread_id = input(
        "Enter customer ID / conversation ID: "
    ).strip()

    if not thread_id:
        thread_id = "customer-001"

    config = {
        "configurable": {
            "thread_id": thread_id
        }
    }

    display_history(app, config)

    print("\nType 'exit' to close the application.")

    try:
        while True:
            user_input = input("\nCustomer: ").strip()

            if user_input.lower() == "exit":
                break

            if not user_input:
                print("Please enter a message.")
                continue

            result = app.invoke(
                {"user_input": user_input},
                config=config
            )

            print("\n========== SUPPORT RESPONSE ==========")
            print("Issue category:", result["category"])
            print("Response:", result["response"])

            print("\nCrewAI review:")
            print(result["crew_notes"])

            log_support_run(
                category=result["category"],
                response=result["response"],
                thread_id=thread_id
            )

    finally:
        connection.close()
        print("\nConversation saved. Application closed.")


if __name__ == "__main__":
    main()
