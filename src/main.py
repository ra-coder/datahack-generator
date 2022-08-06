from random import randint
from typing import Dict

from pyspark.sql import SparkSession

from database import db_default
from generators.float import rand_float_generator, rand_timestamp_generator
from generators.int import rand_int_generator
from generators.float import rand_float_generator
from generators.sample_choice import rand_sample_generator
from generators.str import rand_str_generator


def generate_random_data_v0(input_class, count: int):
    for _ in range(count):
        raw_data = dict()
        for key, key_class in input_class.__annotations__.items():
            if key_class == int:
                raw_data[key] = randint(0, 1000)
            elif key_class == str:
                raw_data[key] = 'aabs'
        res = input_class(**raw_data)
        yield res


GENERATOR_MAP = {
    'int': {
        'generator_type_to_gen': {
            'range': rand_int_generator,
            'choice': rand_sample_generator,
        },
        'default': rand_int_generator,
    },
    'str': {
        'generator_type_to_gen': {
            'random': rand_str_generator,
        },
        'default': rand_str_generator,
    },
    'float': {
        'generator_type_to_gen': {
            'random': rand_float_generator,
            'range': rand_timestamp_generator,
        },
        'default': rand_float_generator,
    },
}


def generate_random_data_v1(input_class, count: int, columns_config: Dict):
    key_to_generator = {}
    for key, key_class in input_class.__annotations__.items():
        if key_class == int:
            gen_map = GENERATOR_MAP['int']
        elif key_class == str:
            gen_map = GENERATOR_MAP['str']
        elif key_class == float:
            gen_map = GENERATOR_MAP['float']
        else:
            raise NotImplementedError

        if key not in columns_config:
            gen = gen_map['default']
            params = {}
        else:
            requested_type = columns_config[key]['generator_type']
            if requested_type not in gen_map['generator_type_to_gen']:
                raise NotImplementedError
            gen = gen_map['generator_type_to_gen'][requested_type]
            params = columns_config[key].get('params', {})
        key_to_generator[key] = gen(**params)

    for _ in range(count):
        yield input_class(
            **{
                key: next(gen) for key, gen in key_to_generator.items()
            }
        )


if __name__ == '__main__':
    spark = SparkSession.builder.appName("data hack").config(
        "spark.driver.host", "localhost"
    ).getOrCreate()
    for table_class, table_config in db_default.items():
        df = spark.createDataFrame(
            generate_random_data_v1(
                table_class,
                count=table_config['count'],
                columns_config=table_config['columns'],
            )
        )
        df.show()
        df.write.parquet(f"output/{table_config['table_name']}.parquet")
    spark.stop()
