# Таблица, для которой будут генерироваться синтетические данные, должна быть описана в отдельном python-скрипте.

from database.user import User, user_default_config
from generators import DBGenerator
from pyspark.sql import SparkSession

TEST_DB_DESCRIPTION = {
    'join_keys': {},
    'tables': {
        User: user_default_config,
    },
}


def test_0_a():
    spark = SparkSession.builder.appName("test_0_a").config(
        "spark.driver.host", "localhost"
    ).getOrCreate()

    # generate
    result_path_info = DBGenerator(spark, TEST_DB_DESCRIPTION).generate_database()

    # test data created

    df = spark.read.parquet(result_path_info["user"])
    df.show(5)
    spark.stop()
