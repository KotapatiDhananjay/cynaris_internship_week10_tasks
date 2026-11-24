import uuid

from langgraph.types import Command
from src.graph import graph


def run_agent(user_input: str):
    """Execute, pause, and resume the LangGraph workflow."""

    config = {
        "configurable": {
            "thread_id": str(uuid.uuid4())
        }
    }

    print("\n========== LANGGRAPH AGENT ==========")
    print("Input:", user_input)

    # First execution: graph pauses at interrupt().
    result = graph.invoke(
        {"user_input": user_input},
        config=config,
    )

    if result.get("__interrupt__"):
        interrupt_data = result["__interrupt__"][0].value

        print("\n========== HUMAN REVIEW ==========")
        print("Message:", interrupt_data["message"])
        print("Category:", interrupt_data["category"])
        print("Input:", interrupt_data["user_input"])

        while True:
            decision = input("\nEnter approve or reject: ").strip().lower()

            if decision in ("approve", "reject"):
                break

            print("Please enter only approve or reject.")

        # Resume using the SAME thread ID.
        result = graph.invoke(
            Command(resume=decision),
            config=config,
        )

    print("\n========== FINAL RESULT ==========")
    print("Category:", result.get("category"))
    print("Human Decision:", result.get("human_decision"))
    print("Status:", result.get("status"))
    print("Response:", result.get("response", "Request stopped."))

    return result


if __name__ == "__main__":
    print("LANGGRAPH - STATEFUL AGENT GRAPH")
    print("Type 'exit' to stop.")

    while True:
        query = input("\nEnter your message: ").strip()

        if query.lower() == "exit":
            print("Program stopped.")
            break

        if not query:
            print("Please enter a message.")
            continue

        run_agent(query)