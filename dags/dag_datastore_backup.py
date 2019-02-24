from airflow import DAG
from airflow.contrib.operators.datastore_export_operator import DatastoreExportOperator
from datetime import datetime, timedelta
from pathlib import Path

# Uncomment to use Slack alert: https://github.com/tszumowski/airflow_slack_operator
#from slack_operator import task_fail_slack_alert


class MyDatastoreExportOperator(DatastoreExportOperator):
    """ 
    Wrapper class to expose the Cloud Storage namespace (directory) as a template.
    That way we can create directories with a timestamped name.
    """
    template_fields = tuple(["namespace"])


default_args = {
    "owner": "airflow",
    "depends_on_past": False,
    "start_date": datetime(2019, 2, 21),  # Change to whatever start date you prefer
    "email": ["email@email.com"],
    "email_on_failure": True,
    "email_on_retry": True,
    "retries": 3,  # Change retry settings for how many times it should try to export
    "retry_delay": timedelta(minutes=5),  
    #"on_failure_callback": task_fail_slack_alert,  # Uncomment to use Slack alert (see above)
}

# Create the DAG with the parameters and schedule
# This just names the dag the filename "dag_datastore_backup", without extension
dag_name = Path(__file__).stem
dag = DAG(
    dag_name,
    catchup=False,  # Don't forget this so that it doesn't run and backfill since start date
    default_args=default_args,
    schedule_interval=timedelta(days=1),  # Run daily
)

# Create the DAG with a single task here
with dag:
    # Access excution date template
    execution_date = "{{ execution_date }}"

    # Create the Datastore Export task. Create a new 
    # ISO 8601 timestamped directory for each backup
    t1 = MyDatastoreExportOperator(
        task_id="datastore_export",
        bucket="bucket-name",
        namespace="archive/exports/datastore/{}".format(execution_date),
        overwrite_existing=True,
    )
