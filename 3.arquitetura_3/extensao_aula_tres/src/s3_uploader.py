import json
import boto3
import logging

from datetime import datetime

class S3_Uploader:

	logging.getLogger().setLevel(logging.INFO)

	self.client = boto3.client(s3)

	def upload_to_s3(self, bucket, schema, table, partition, json_data) -> Any:
		"""
		Uploading data to s3 :D
		"""
		now: datetime.date = datetime.now()
		now_string: str = now.strftime("%Y-%m-%d-%H-%M-%S") 
		key: str = f"{schema}/table/date={partition}/{schema}_{table}_{now_string}.json"

		logging.info(f"Uploading file to S3 with key: {key}")

		bin_data = json.dumps(json_data).encode("utf-8")
		return client.put_object(Body=bin_data, Bucket=bucket, Key=key)