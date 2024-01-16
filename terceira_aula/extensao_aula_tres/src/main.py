import yaml
import sys

from typing import NoReturn, Dict
from datetime import datetime
from s3_uploader import upload_to_s3
from api_client import get_daily_summary

class MainEntryPoint:
	def __init__(self, date):
		self.year = datetime.strftime('%Y')
		self.month = datetime.strftime('%m')
		self.day = datetime.strftime('%d')

	def extract_and_upload(self) -> NoReturn:
		for coin in config['coins']:
 		json_data = get_daily_summary(coin, int(self.year), int(self.month), int(self.day))
 		upload_to_s3(
 			bucket=config['bucket'],
 			schema=config['schema'],
 			table=coin,
 			partition=date.strftime('%Y-%m-%d'),
 			json_data=json_data
 		)

if __name__ == "__main__":
	date = datetime.strptime(sys.argv[1], '%Y-%m-%d')
	entry_point: Any = MainEntryPoint(date)

	with open("config.yml") as f:
		confi: Dict = yaml.safe_load(f)

	entry_point.extract_and_upload()




