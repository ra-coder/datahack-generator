from pyspark.sql import SparkSession

spark = SparkSession.builder.appName("data hack").config(
    "spark.driver.host", "localhost"
).getOrCreate()

for name in ['user', 'schedule', 'company', 'category']:
    df = spark.read.parquet(f"output/{name}.parquet")
    df.show()
spark.stop()
