# your_dag_file.py

from airflow import DAG
from airflow.operators.python_operator import PythonOperator
from datetime import datetime
from app import start_flask_app  # Importez la fonction de démarrage Flask depuis le chemin complet

default_args = {
    'owner': 'zana',
    'start_date': datetime(2023, 1, 1),
    'retries': 1,
}

dag = DAG(
    'monumentDAG',
    default_args=default_args,
    schedule_interval='@daily',
)

task = PythonOperator(
    task_id='start_flask_app_task',
    python_callable=start_flask_app,  # Appelez la fonction de démarrage Flask depuis le chemin complet
    dag=dag,
)
