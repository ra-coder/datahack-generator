"""
    test_2_a Генерация двух таблиц с полным пересечением по ключу объединения:
            Одно поле в качестве ключа объединения

    test_2_b Генерация двух таблиц с полным пересечением по ключу объединения:
            Три поля в качестве ключа объединения
"""

from database import DB_DESCRIPTION
from database.user import User, user_default_config
from database.user_bio import UserBio, user_bio_default_config
from generators import DBGenerator
from pyspark.sql import SparkSession, functions


def test_2_a():
    test_DB_DESCRIPTION = {
        'join_keys': {
            'user_id': {
                'primary_keys': {
                    'table_name': 'user',
                    'column_names': ['id'],
                },
                'secondary_use': [
                    {
                        'table_name': 'user_bio',
                        'column_names': ['user_id'],
                    }
                ],
            }
        },
        'tables': {
            User: user_default_config,
            UserBio: user_bio_default_config,
        },
    }

    spark = SparkSession.builder.appName("test_0_a").config(
        "spark.driver.host", "localhost"
    ).getOrCreate()
    # generate
    result_path_info = DBGenerator(spark, test_DB_DESCRIPTION).generate_database()

    # test data created
    df_user = spark.read.parquet(result_path_info["user"])
    df_user.show(5)
    df_bio = spark.read.parquet(result_path_info["user_bio"])

    user_ids = set(df_user.select(functions.collect_list('id')).first()[0])

    for rec in df_bio.select(functions.collect_list('user_id')).first()[0]:
        assert rec in user_ids

    spark.stop()


if __name__ == '__main__':
    test_2_a()
