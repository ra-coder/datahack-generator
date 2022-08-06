from typing import Dict
import json
import logging
import time
import shutil

from pyspark.sql import SparkSession

from database import db_default
from database.types import TimeStamp
from generators.float import rand_float_generator
from generators.int import rand_int_generator, mask_int_generator
from generators.sample_choice import rand_sample_generator
from generators.str import rand_str_generator, mask_str_generator
from generators.timestamp import rand_timestamp_generator

GENERATOR_MAP = {
    'int': {
        'generator_type_to_gen': {
            'range': rand_int_generator,
            'choice': rand_sample_generator,
            'mask': mask_int_generator,
        },
        'default': rand_int_generator,
    },
    'str': {
        'generator_type_to_gen': {
            'random': rand_str_generator,
            'choice': rand_sample_generator,
            'mask': mask_str_generator,
        },
        'default': rand_str_generator,
    },
    'float': {
        'generator_type_to_gen': {
            'random': rand_float_generator,
            'range': rand_float_generator,
            'choice': rand_sample_generator,
        },
        'default': rand_float_generator,
    },
    'timestamp': {
        'generator_type_to_gen': {
            'random': rand_timestamp_generator,
            'range': rand_timestamp_generator,
            'choice': rand_sample_generator,
        },
        'default': rand_timestamp_generator,
    },

}


def generate_random_rows(input_class, count: int, columns_config: Dict, columns_override_conf: Dict):
    key_to_generator = {}
    for key, key_class in input_class.__annotations__.items():
        if key_class == int:
            gen_map = GENERATOR_MAP['int']
        elif key_class == str:
            gen_map = GENERATOR_MAP['str']
        elif key_class == float:
            gen_map = GENERATOR_MAP['float']
        elif key_class == TimeStamp:
            gen_map = GENERATOR_MAP['timestamp']
        else:
            raise NotImplementedError(f'No generator for {key_class}')

        column_cfg = columns_override_conf.get(key) or columns_config.get(key)

        if column_cfg is None:
            gen = gen_map['default']
            params = {}
        else:
            requested_type = column_cfg['generator_type']
            if requested_type not in gen_map['generator_type_to_gen']:
                raise NotImplementedError
            gen = gen_map['generator_type_to_gen'][requested_type]
            params = column_cfg.get('params', {})
        key_to_generator[key] = gen(**params)

    for _ in range(count):
        yield input_class(
            **{
                key: next(gen) for key, gen in key_to_generator.items()
            }
        )


if __name__ == '__main__':
    with open('../data_cfg.json', 'r') as fp:
        override_conf = json.load(fp)

    spark = SparkSession.builder.appName("data hack").config(
        "spark.driver.host", "localhost"
    ).getOrCreate()
    logging.warning('START sample generation')
    start = time.time()
    for table_class, table_config in db_default.items():
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
