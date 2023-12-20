from airflow import DAG
from airflow.operators.bash_operator import BashOperator
from datetime import datetime, timedelta

default_args = {
    'owner': 'zana',
    'start_date': datetime(2023, 12, 12),
    'retries': 1,
    'retry_delay': timedelta(minutes=5),
}

dag = DAG(
    'monument_dag',
    default_args=default_args,
    description='Expose web page via Airflow',
    schedule_interval=timedelta(days=1),  # Définissez la fréquence d'exécution
)

# Assurez-vous que le chemin du fichier DAG est correct
dag_folder = r'C:/Users/parduzizana/airflow/dags'

# Assurez-vous que le chemin du fichier app.py est correct
app_path = r"C:/Users/parduzizana/Documents/INFO_5A/Big Data/opendata/app.py"

preparation_task = BashOperator(
    task_id='preparation_task',
    bash_command='echo "Perform preparation"',
    dag=dag,
)

expose_web_page_task = BashOperator(
    task_id='expose_web_page',
    bash_command=f'python {app_path}',  # Commande pour exécuter votre script Flask
    dag=dag,
)

preparation_task >> expose_web_page_task  # Définir la dépendance entre les tâches
