from pyspark.sql import SparkSession

spark = SparkSession.builder.appName("data hack").config(
    "spark.driver.host", "localhost"
    # ).config(
    #     "spark.driver.port", "7077"
).getOrCreate()

df = spark.read.parquet("output/user.parquet")
df.show()
spark.stop()
