import uuid

from langgraph.types import Command
from src.state_machine import state_machine


def execute_state_machine(user_input):
    config = {
        "configurable": {
            "thread_id": str(uuid.uuid4())
        }
    }

    print("\n========== STATE MACHINE ==========")
    print("User input:", user_input)

    # Start execution
    result = state_machine.invoke(
        {"user_input": user_input},
        config=config,
    )

    # Check whether the graph was interrupted
    if result.get("__interrupt__"):
        details = result["__interrupt__"][0].value

        print("\n========== HUMAN REVIEW ==========")
        print("Category:", details["category"])
        print("Input:", details["input"])
        print("Available decisions:", details["available_decisions"])

        while True:
            decision = input("Enter approve or reject: ").strip().lower()

            if decision in ["approve", "reject"]:
                break

            print("Invalid decision. Enter approve or reject.")

        # Resume using the same thread ID
        result = state_machine.invoke(
            Command(resume=decision),
            config=config,
        )

    print("\n========== STATE MACHINE RESULT ==========")
    print("Category:", result.get("category"))
    print("Human decision:", result.get("human_decision"))
    print("Status:", result.get("status"))
    print("Response:", result.get("response", "No response generated."))

    return result


if __name__ == "__main__":
    print("LANGGRAPH STATE MACHINES & CONDITIONAL EDGES")
    print("Type exit to stop.")

    while True:
        user_input = input("\nEnter your message: ").strip()

        if user_input.lower() == "exit":
            print("Application closed.")
            break

        if not user_input:
            print("Please enter a message.")
            continue

        execute_state_machine(user_input)