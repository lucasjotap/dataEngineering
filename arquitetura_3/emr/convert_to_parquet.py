from pyspark.sql import SparkSession

spark = SparkSession \
		.builder \
		.appName("to_parquet") \
		.getOrCreate()

for coin in ['BTC', 'BCH', 'ETH', 'LTC']:
	df = spark.read.format('json').load("path")
	df.write.format('parquet').save(path="path", mode='overwrite')