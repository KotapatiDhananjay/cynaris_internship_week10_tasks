from crewai import Agent, Task, Crew, Process, BaseLLM


class OfflineSupportLLM(BaseLLM):
    """
    Simple deterministic local LLM.
    This avoids external API keys and cloud model calls.
    """

    def __init__(self):
        super().__init__(model="offline/customer-support")

    def call(
        self,
        messages,
        tools=None,
        callbacks=None,
        available_functions=None,
        from_task=None,
        from_agent=None,
        response_model=None,
        **kwargs
    ):
        role = getattr(from_agent, "role", "Support Agent")

        if "Triage" in role:
            return "Triage completed. The customer issue was reviewed and categorized."

        if "Resolution" in role:
            return "Resolution plan reviewed. Follow the supplied support policy and provide clear next steps."

        if "Quality" in role:
            return "Quality review passed. The response should be relevant, safe, and based on the supplied policy."

        return "Customer support review completed."


def run_support_crew(user_input, category, context):
    """Run three specialized CrewAI agents sequentially."""

    local_llm = OfflineSupportLLM()

    triage_agent = Agent(
        role="Support Triage Analyst",
        goal="Review and understand customer issues.",
        backstory="You are an experienced customer support triage specialist.",
        llm=local_llm,
        verbose=False,
        allow_delegation=False,
        max_iter=1,
        max_retry_limit=0
    )

    resolution_agent = Agent(
        role="Support Resolution Specialist",
        goal="Review the policy and identify suitable next steps.",
        backstory="You specialize in customer issue resolution.",
        llm=local_llm,
        verbose=False,
        allow_delegation=False,
        max_iter=1,
        max_retry_limit=0
    )

    quality_agent = Agent(
        role="Support Quality Reviewer",
        goal="Check that the proposed support handling is clear and safe.",
        backstory="You review customer support responses for quality.",
        llm=local_llm,
        verbose=False,
        allow_delegation=False,
        max_iter=1,
        max_retry_limit=0
    )

    triage_task = Task(
        description=(
            "Review this customer issue: {user_input}. "
            "Its detected category is {category}. "
            "Summarize the issue."
        ),
        expected_output="A short triage summary.",
        agent=triage_agent
    )

    resolution_task = Task(
        description=(
            "Review the customer issue: {user_input}. "
            "Use this policy context: {context}. "
            "Describe the appropriate resolution approach."
        ),
        expected_output="A short resolution plan.",
        agent=resolution_agent
    )

    quality_task = Task(
        description=(
            "Review the support handling for this issue: {user_input}. "
            "Check that the process is safe, clear, and policy-based."
        ),
        expected_output="A short quality review.",
        agent=quality_agent
    )

    crew = Crew(
        agents=[triage_agent, resolution_agent, quality_agent],
        tasks=[triage_task, resolution_task, quality_task],
        process=Process.sequential,
        verbose=False
    )

    result = crew.kickoff(
        inputs={
            "user_input": user_input,
            "category": category,
            "context": context
        }
    )

    return str(result)