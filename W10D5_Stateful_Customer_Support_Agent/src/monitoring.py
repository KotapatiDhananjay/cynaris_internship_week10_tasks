import mlflow


def log_support_run(category, response, thread_id):
    """Track customer support workflow performance in MLflow."""

    mlflow.set_tracking_uri("sqlite:///mlflow.db")
    mlflow.set_experiment("W10D5_Stateful_Customer_Support")

    with mlflow.start_run():
        mlflow.log_param("issue_category", category)
        mlflow.log_param("thread_id", thread_id)
        mlflow.log_param("workflow", "LangGraph + CrewAI")

        mlflow.log_metric("response_length", float(len(response)))
        mlflow.log_metric("response_generated", 1.0 if response else 0.0)

        mlflow.set_tag("project", "W10D5")
        mlflow.set_tag("environment", "local")

        print("[MLflow] Run and metrics logged successfully.")