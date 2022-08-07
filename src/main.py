import json
import logging
import time

from pyspark.sql import SparkSession

from database import DB_DESCRIPTION
from generators import DBGenerator


if __name__ == '__main__':
    with open('../data_cfg.json', 'r') as fp:
        override_conf = json.load(fp)

    spark = SparkSession.builder.appName("data hack").config(
        "spark.driver.host", "localhost"
    ).getOrCreate()
    logging.warning('START sample generation')
    start = time.time()

    DBGenerator(DB_DESCRIPTION, override_conf, spark).generate_database()

    logging.warning('END sample generation. Time consumed %r', time.time() - start)
    spark.stop()
