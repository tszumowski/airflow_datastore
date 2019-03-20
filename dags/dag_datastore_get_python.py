""" dag_datastore_get_python.py
Uses native Airflow PythonOperator to get a field from a Datastore Kind

"""
from airflow import DAG
from datetime import datetime, timedelta
from airflow.operators.python_operator import PythonOperator
from pathlib import Path
from google.cloud import datastore


def get_last_update(project, namespace, kind, timestamp_prop="timestamp", **kwargs):
    """
    Direct Python function to get the last update time found in a Datastore kind,
    as an example of a simple GET operation. Assume AUTH is taken care of outside of
    the codebase.

    Args:
        project (str): GCP Project name
        namespace (str): Namespace in Datastore
        kind (str): Kind to get from
        timestamp_prop (str): Name of property that holds timestamp

    Returns:
        last_update (str): Last commit timestamp for that kind

    """
    # Get a client object
    client = datastore.Client(project=project, namespace=namespace)
    # Build a query that gets most recent key and orders by timestamp descending
    query = client.query(kind=kind, order=[f"-{timestamp_prop}"])
    result = list(query.fetch(1))[0]
    print(result)

    # Pull out timestamp. In Datastore, it returns as string
    last_update = str(result[timestamp_prop])
    print(f"Last Update Time: {last_update}")
    return last_update


"""
Airflow defaults
"""
default_args = {
    "owner": "airflow",
    "depends_on_past": False,
    "start_date": datetime(2019, 3, 19),  # Change to whatever start date you prefer
    "email": ["email@email.com"],
    "email_on_failure": True,
    "email_on_retry": True,
    "retries": 3,  # Change retry settings for how many times it should try
    "retry_delay": timedelta(minutes=5),
}

# Create the DAG with the parameters and schedule
# This just names the dag the filename "dag_datastore_backup", without extension
dag_name = Path(__file__).stem
dag = DAG(
    dag_name,
    catchup=False,  # Don't forget this so that it doesn't run and backfill since start
    default_args=default_args,
    schedule_interval=timedelta(days=1),  # Run daily
)

# TODO: Insert variables here!
# WARNING: In operations, this should be pulled in from Airflow Variables instead
PROJECT = "<PROJECT>"
NAMESPACE = "<NAMESPACE>"
KIND = "<KIND>"

# Create the DAG with a single task here
with dag:
    # Create the PythonOperator task
    t1 = PythonOperator(
        task_id="get_last_update_test_kind",
        provide_context=True,
        python_callable=get_last_update,
        op_args=[PROJECT, NAMESPACE, KIND],
    )
