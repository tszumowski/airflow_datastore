# Airflow Datastore Examples

This provides example usage for the Airflow Google Cloud Datastore Export Operator. 

This Medium article, [Perform Daily Backups of Your Google Cloud Datastore using Airflow](https://medium.com/@tszumowski/slack-alerts-in-airflow-1fc16f322b51](https://medium.com/@tszumowski/perform-daily-backups-of-your-google-cloud-datastore-using-airflow-ec763b71c4a1), describes this code with some visuals.

# Usage

This assumes you already have Airflow running. 

## (Optional) Initial Local Tests
These are optional, but helps ensure a healthy DAG before launching it. Run these on a local airflow instance before saving them to a final deployed one.

1. Install airflow locally: `pip install -r requirements.txt`. This gives you access to `airflow` commands in later steps.
2. Copy the contents of `dags` into your local airflow `dags` directory
3. Confirm DAG compiles with: `python dags/dag_datastore_backup.py`
4. Confirm it can be bagged: `airflow initdb`.
5. Confirm the task can be run: `airflow test dag_datastore_backup datastore_export 2019-01-01`
    - This will only work if you have connection IDs and credentials set up in your local Airflow installation. However you may still be able to see it run some of the DAG.

## Installation and Running
Similar to other Airflow DAGs, just copy the contents of `dags` into your deployed Airflow `dags` directory.

## (Optional) Install Slack Webhooks
1. Uncomment the noted lines in `dag_datastore_backup.py`
2. Copy `slack_operator.py` into your DAGs directory, found [here](https://github.com/tszumowski/airflow_slack_operator)
3. Follow `README` found in that link for installing Slack Alerts
