from langgraph.types import Command
from src.human_loop import build_graph


def main():
    app = build_graph()

    print("\n========================================")
    print(" LANGGRAPH HUMAN-IN-THE-LOOP SYSTEM")
    print("========================================")

    while True:
        user_input = input("\nEnter your message (or 'exit'): ").strip()

        if user_input.lower() == "exit":
            print("Application closed.")
            break

        if not user_input:
            print("Please enter a message.")
            continue

        config = {
            "configurable": {
                "thread_id": "human-review-session"
            }
        }

        initial_state = {
            "user_input": user_input
        }

        try:
            result = app.invoke(initial_state, config=config)

            # The graph pauses at the human approval interrupt.
            if result.get("__interrupt__"):
                print("\n[HUMAN REVIEW REQUIRED]")
                print(f"Category: {result['__interrupt__'][0].value['category']}")
                print(f"Input: {user_input}")

                decision = input(
                    "Enter approve or reject: "
                ).strip().lower()

                while decision not in ["approve", "reject"]:
                    decision = input(
                        "Invalid choice. Enter approve or reject: "
                    ).strip().lower()

                # Resume the same graph execution.
                result = app.invoke(
                    Command(resume=decision),
                    config=config
                )

            print("\n--------------- RESULT ---------------")
            print("Category:", result.get("category"))
            print("Decision:", result.get("human_decision", "Not required"))
            print("Status:", result.get("status"))
            print("Response:", result.get("response", "No response generated."))

        except Exception as error:
            print("An error occurred:", error)


if __name__ == "__main__":
    main()