from pyspark.sql import SparkSession

spark = SparkSession.builder.appName("ReadParquet").getOrCreate()

df = spark.read.parquet("/home/home/Desktop/aws-data-engineer-project/parquet_downloads/processed/sales")

df.show()