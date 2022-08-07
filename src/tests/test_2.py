"""
    test_2_a Генерация двух таблиц с полным пересечением по ключу объединения:
            Одно поле в качестве ключа объединения

    test_2_b Генерация двух таблиц с полным пересечением по ключу объединения:
            Три поля в качестве ключа объединения
"""

from database.user import User, user_default_config
from database.user_bio import UserBio, user_bio_default_config
from database.schedule import Schedule, schedule_default_config
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


def test_2_b():
    test_DB_DESCRIPTION = {
        'join_keys': {
            'user_info': {
                'primary_keys': {
                    'table_name': 'user',
                    'column_names': ['id', 'birthday', 'label2'],
                },
                'secondary_use': [
                    {
                        'table_name': 'schedule',
                        'column_names': ['user_id', 'user_birthday', 'label2'],
                    }
                ],
            },
        },
        'tables': {
            User: user_default_config,
            Schedule: schedule_default_config,
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
    df_schedule = spark.read.parquet(result_path_info["schedule"])

    # TODO spark check
    # for rec in df_schedule.sample(False, 0.1, seed=0).limit(10):
    #     print(rec)
    #     print(rec.user_id.value)
    #     user = df_user.filter(
    #         df_user.id == rec.user_id
    #     ).filter(
    #         df_user.birthday == rec.user_birthday
    #     ).filter(
    #         df_user.label2 == rec.label2
    #     ).first()
    #     print(user)
    #     assert user is not None

    spark.stop()


if __name__ == '__main__':
    test_2_b()
