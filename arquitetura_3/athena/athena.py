import pandas as pd 

from pyathena import connect
from typing import NoReturn
from pandas import DataFrame 

class DataReaderFromAthena(object):
	"""DataReaderFromAthena lidará com queries vindo do Athena."""
	conn: object = None
	pd.set_option("display.width", 420)
	pd.set_option("display.max_columns", 15)

	def establish_connection(self) -> object:
		return self.conn: object = connect(work_group='athena-data-engineer-workgroup')

	def read_sql(self) -> NoReturn:
		self.establish_connection()
		query: str = "select * from data_lake_raw.titanic"
		df: DataFrame = pd.read_sql(query, conn)
		print(df.head())