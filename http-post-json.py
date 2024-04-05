from datetime import datetime, timedelta
from airflow import DAG
from airflow.providers.http.operators.http import SimpleHttpOperator
from airflow.operators.dummy_operator import DummyOperator

default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'email_on_failure': False,
    'email_on_retry': False,
    'retries': 1,
    'retry_delay': timedelta(minutes=5),
}

dag = DAG(
    'http_post_example',
    default_args=default_args,
    description='A simple HTTP POST example',
    schedule_interval=timedelta(days=1),
    start_date=datetime(2023, 1, 1),
    catchup=False,
)

post_json = SimpleHttpOperator(
    task_id='post_json',
    http_conn_id='http_default',
    endpoint='api/data',
    method='POST',
    headers={"Content-Type": "application/json"},
    data=json.dumps({
        "key": "value",
        "another_key": "another_value"
    }),
    dag=dag,
)

start = DummyOperator(task_id='start', dag=dag)

start >> post_json
