import logging

from datetime import datetime
from airflow import DAG
from airflow.contrib.operators.aws_athena_operator import AWSAthenaOperator

logger = logging.getLogger(__name__)

default_args = {
	"owner":"lucas",
	"start_date":datetime(2020, 5, 20),
	"dependes_on_past": False,
	"provide_context": True
}


query =  """			WITH step_one AS (
			  SELECT 
			    user_domain_id, 
			    date_parse(
			      event_timestamp, '%Y-%m-%d %h:%i:%s.%f'
			    ) as timestamp, 
			    LAG(
			      date_parse(
			        event_timestamp, '%Y-%m-%d %h:%i:%s.%f'
			      ), 
			      1
			    ) OVER (
			      PARTITION BY user_domain_id 
			      ORDER BY 
			        event_timestamp
			    ) AS previous_timestamp 
			  FROM 
			    data_lake_raw.atomic_events
			), 
			step_two AS (
			  SELECT 
			    user_domain_id, 
			    timestamp, 
			    previous_timestamp, 
			    CASE WHEN date_diff(
			      'minute', previous_timestamp, timestamp
			    ) >= 30 THEN 1 ELSE 0 END AS new_session 
			  FROM 
			    step_one
			), 
			step_three AS (
			  SELECT 
			    user_domain_id, 
			    timestamp, 
			    previous_timestamp, 
			    new_session, 
			    SUM(new_session) OVER (
			      PARTITION BY user_domain_id 
			      ORDER BY 
			        timestamp ROWS BETWEEN UNBOUNDED PRECEDING 
			        AND CURRENT ROW
			    ) AS session_idx 
			  FROM 
			    step_two
			) 
			SELECT 
			  user_domain_id || CAST(session_idx AS VARCHAR) AS session_id, 
			  * 
			FROM 
			  step_three;
"""

with DAG ('sessions',
		   description='DAG pra sessionizar usuarios',
		   schedule_interval="* /15 * * * *", 
		   catchup=False,
		   default_args=default_args
		   ) as dag:
	
	t1 = AWSAthenaOperator(
		task_id="sessionization",
		dag=dag,
		query=query,
		database="data_lake_raw",
		output_location="s3://s3-aloha-prod-data-lake_curated/sessions-airflow",
		aws_conn_id="aws_default"
		)