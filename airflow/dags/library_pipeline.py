from datetime import datetime, timedelta

from airflow import DAG
from airflow.operators.bash import BashOperator


PROJECT_DIR = "/opt/airflow/project"


default_args = {
    "owner": "Meshal",
    "retries": 2,
    "retry_delay": timedelta(minutes=2),
}


dag_description = """
# Jeddah Library Demand Training Pipeline

This pipeline runs the machine learning workflow for the Jeddah Library Demand Advisor project.

It performs three main steps:

1. Preprocess the raw library rental dataset.
2. Train and evaluate multiple machine learning models.
3. Run a sample prediction to validate that the saved model works.

The goal is to automate the model training workflow and make the project closer to a real production-style machine learning system.
"""


with DAG(
    dag_id="library_demand_training_pipeline",
    description="Automated ML training pipeline for Jeddah library demand prediction.",
    doc_md=dag_description,
    default_args=default_args,
    start_date=datetime(2026, 5, 25),
    schedule="@daily",
    catchup=False,
    tags=["library-demand", "machine-learning", "airflow"],
) as dag:

    preprocess_library_data = BashOperator(
        task_id="preprocess_library_data",
        bash_command=f"cd {PROJECT_DIR} && python src/clean_data.py",
    )

    train_and_evaluate_models = BashOperator(
        task_id="train_and_evaluate_models",
        bash_command=f"cd {PROJECT_DIR} && python src/train_model.py",
    )

    validate_prediction_output = BashOperator(
        task_id="validate_prediction_output",
        bash_command=f"cd {PROJECT_DIR} && python src/predict.py",
    )

    preprocess_library_data >> train_and_evaluate_models >> validate_prediction_output