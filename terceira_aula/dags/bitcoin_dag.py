import logging

from datetime import datetime

from airflow import DAG
from airflow.contrib.operators.ecs_operator import ECSOperator
from airflow.models import Variable

logger = logging.getLogger(__name__)

default_args: dict = {
	'owner':'lucas',
	'start_date': datetime(2024, 1, 15),
	'depends_on_past': False, 
	'provide_context': True
}

execution_date = '{{ ds }}'

with DAG("bitcoin_dag",
	description='DAG to extract Daily Summaries from MercadoBitcoin',
	schedule_interval='0 1 * * * *',
	catchup=True,
	default_args=default_args
	) as dag:

	t1 = ECSOperator(
		task_id="crypto_extract",
		dag=dag,
		aws_conn_id="aws_default",
		cluster="airflow-production-ecs-cluster",
		task_definition="production-crypto-extract-image",
		launch_type="FARGATE",
		overrides={
			"containerOverrides": [
				{
					"name": "production-crypto-extract-image",
					"command": ["python", "main.py", execution_date],
				}
			],
		},

		network_configuration = {
			"awsvpcConfiguration": {
				"securityGroups": [Variable.get("security-group")],
				"subnets": [Variable.get("subnet")],
				"assignPublicIp": "ENABLED"
			}
		}
	)