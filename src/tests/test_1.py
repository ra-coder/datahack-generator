"""
 Генерация нескольких различных таблиц с полным (и не полным) набором столбцов заданных типов данных и
    различными настройками для значений полей (диапазон, набор значений, маска).
    -Кол-во строк: 10 000
"""

from database import DB_DESCRIPTION
from generators import DBGenerator
from pyspark.sql import SparkSession


def test_1():
    spark = SparkSession.builder.appName("test_0_a").config(
        "spark.driver.host", "localhost"
    ).getOrCreate()

    recs_count = 0
    for table_desc in DB_DESCRIPTION['tables'].values():
        recs_count += table_desc['count']

    assert recs_count > 10000

    # generate
    result_path_info = DBGenerator(spark, DB_DESCRIPTION).generate_database()

    # test data created
    df = spark.read.parquet(result_path_info["user"])
    df.show(5)
    spark.stop()
