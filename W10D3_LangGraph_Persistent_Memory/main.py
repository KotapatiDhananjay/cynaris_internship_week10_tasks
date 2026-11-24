from langgraph.types import Command

from src.memory_graph import create_sqlite_graph


def display_history(app, config):
    """Display the conversation history saved for this thread."""

    snapshot = app.get_state(config)
    values = snapshot.values

    print("\n========== SAVED CONVERSATION ==========")

    messages = values.get("messages", [])

    if not messages:
        print("No previous messages.")
        return

    for message in messages:
        role = message.get("role", "unknown").upper()
        content = message.get("content", "")
        print(f"{role}: {content}")


def run_conversation(app, thread_id):
    """Run or continue a persistent conversation."""

    config = {
        "configurable": {
            "thread_id": thread_id
        }
    }

    display_history(app, config)

    print("\nEnter 'exit' to return to the conversation menu.")

    while True:
        user_input = input("\nYou: ").strip()

        if user_input.lower() == "exit":
            break

        if not user_input:
            print("Please enter a message.")
            continue

        result = app.invoke(
            {"user_input": user_input},
            config=config,
        )

        if result.get("__interrupt__"):
            details = result["__interrupt__"][0].value

            print("\n========== HUMAN REVIEW ==========")
            print("Category:", details["category"])
            print("Request:", details["input"])

            while True:
                decision = input(
                    "Enter approve or reject: "
                ).strip().lower()

                if decision in ["approve", "reject"]:
                    break

                print("Enter approve or reject.")

            result = app.invoke(
                Command(resume=decision),
                config=config,
            )

        print("\n========== RESULT ==========")
        print("Category:", result.get("category"))
        print("Decision:", result.get("human_decision"))
        print("Status:", result.get("status"))
        print("Response:", result.get("response", "No response generated."))

        display_history(app, config)


def main():
    app, connection = create_sqlite_graph()

    print("LANGGRAPH - PERSISTENT CONVERSATION MEMORY")

    try:
        while True:
            print("\n========== CONVERSATION MENU ==========")
            print("1. Start a new conversation")
            print("2. Continue an existing conversation")
            print("3. Exit")

            choice = input("Choose an option: ").strip()

            if choice == "1":
                thread_id = input(
                    "Enter a new conversation ID: "
                ).strip()

                if not thread_id:
                    print("Conversation ID cannot be empty.")
                    continue

                run_conversation(app, thread_id)

            elif choice == "2":
                thread_id = input(
                    "Enter your previous conversation ID: "
                ).strip()

                if not thread_id:
                    print("Conversation ID cannot be empty.")
                    continue

                config = {
                    "configurable": {
                        "thread_id": thread_id
                    }
                }

                snapshot = app.get_state(config)

                if not snapshot.values:
                    print("No saved conversation found.")
                    continue

                run_conversation(app, thread_id)

            elif choice == "3":
                print("Application closed. Conversation data is saved.")
                break

            else:
                print("Invalid choice. Select 1, 2, or 3.")

    finally:
        connection.close()


if __name__ == "__main__":
    main()