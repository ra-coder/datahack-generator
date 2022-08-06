import json
import logging
import time
import shutil

from pyspark.sql import SparkSession

from database import DB_DESCRIPTION
from generators import generate_random_rows

if __name__ == '__main__':
    with open('../data_cfg.json', 'r') as fp:
        override_conf = json.load(fp)

    spark = SparkSession.builder.appName("data hack").config(
        "spark.driver.host", "localhost"
    ).getOrCreate()
    logging.warning('START sample generation')
    start = time.time()
    for table_class, table_config in DB_DESCRIPTION.items():
        table_override_conf = override_conf.get(table_config['table_name'], {})
        df = spark.createDataFrame(
            generate_random_rows(
                table_class,
                count=(table_override_conf.get('count') or table_config['count']),
                columns_config=table_config['columns'],
                columns_override_conf=table_override_conf.get('columns', {})
            )
        )
        df.show()
        res_filename = f"output/{table_config['table_name']}.parquet"
        shutil.rmtree(res_filename)
        df.write.parquet(res_filename)

    logging.warning('END sample generation. Time consumed %r', time.time() - start)
    spark.stop()
