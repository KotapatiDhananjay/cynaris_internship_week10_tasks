import csv
from pathlib import Path

import mlflow
from ragas import EvaluationDataset
from ragas.dataset_schema import SingleTurnSample

from src.knowledge_base import (
    KNOWLEDGE_BASE,
    classify_issue,
    build_response,
    retrieve_context
)


TEST_CASES = [
    {
        "question": "Where is my delayed delivery?",
        "reference": KNOWLEDGE_BASE["delivery"]["response"]
    },
    {
        "question": "I want a refund for my order.",
        "reference": KNOWLEDGE_BASE["refund"]["response"]
    },
    {
        "question": "My payment was deducted.",
        "reference": KNOWLEDGE_BASE["payment"]["response"]
    },
    {
        "question": "I cannot login to my account.",
        "reference": KNOWLEDGE_BASE["account"]["response"]
    },
    {
        "question": "My product is damaged.",
        "reference": KNOWLEDGE_BASE["product"]["response"]
    }
]


def calculate_policy_overlap(response, context):
    """Calculate a simple local word-overlap score."""

    response_words = set(response.lower().split())
    context_words = set(context.lower().split())

    if not response_words:
        return 0.0

    matching_words = response_words.intersection(context_words)

    return len(matching_words) / len(response_words)


def main():
    Path("output").mkdir(exist_ok=True)

    samples = []
    results = []

    for case in TEST_CASES:
        question = case["question"]
        category = classify_issue(question)

        context = retrieve_context(category)["context"]
        response = build_response(category)

        score = calculate_policy_overlap(response, context)

        # Build a Ragas-compatible evaluation sample.
        sample = SingleTurnSample(
            user_input=question,
            response=response,
            retrieved_contexts=[context],
            reference=case["reference"]
        )

        samples.append(sample)

        results.append({
            "question": question,
            "category": category,
            "response": response,
            "reference": case["reference"],
            "policy_overlap": round(score, 4)
        })

    # Construct the Ragas evaluation dataset.
    evaluation_dataset = EvaluationDataset(samples=samples)

    output_file = Path("output/customer_support_evaluation.csv")

    with output_file.open(
        "w",
        newline="",
        encoding="utf-8"
    ) as file:
        writer = csv.DictWriter(
            file,
            fieldnames=results[0].keys()
        )
        writer.writeheader()
        writer.writerows(results)

    average_score = sum(
        item["policy_overlap"] for item in results
    ) / len(results)

    mlflow.set_tracking_uri("sqlite:///mlflow.db")
    mlflow.set_experiment("W10D5_Ragas_Evaluation")

    with mlflow.start_run():
        mlflow.log_param("evaluation_framework", "Ragas")
        mlflow.log_param("evaluation_samples", len(evaluation_dataset.samples))
        mlflow.log_metric("average_policy_overlap", average_score)
        mlflow.log_artifact(str(output_file))

    print("\n========== EVALUATION RESULTS ==========")
    print("Evaluation samples:", len(evaluation_dataset.samples))
    print("Average policy overlap:", round(average_score, 4))
    print("Saved:", output_file)


if __name__ == "__main__":
    main()