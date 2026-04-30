from pyspark.sql import SparkSession

spark = SparkSession.builder.appName("ReadParquet").getOrCreate()

df = spark.read.parquet("/home/home/Desktop/aws-data-engineer-project/scripts/parquet_downloads/")

df.show()