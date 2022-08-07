import logging
from datetime import date
from typing import Dict
import shutil
from random import choice

from database.types import TimeStamp
from .float_numbers import rand_float_generator
from .integet import mask_int_generator, rand_int_generator
from .sample_choice import rand_choice_generator, choice_from_foreign_table_column_stab
from .string import mask_str_generator, rand_str_generator
from .timestamp import rand_timestamp_generator
from .dates import rand_date_generator

GENERATOR_MAP = {
    'int': {
        'generator_type_to_gen': {
            'range': rand_int_generator,
            'choice': rand_choice_generator,
            'mask': mask_int_generator,
            'foreign_key': choice_from_foreign_table_column_stab,
        },
        'default': rand_int_generator,
    },
    'str': {
        'generator_type_to_gen': {
            'random': rand_str_generator,
            'choice': rand_choice_generator,
            'mask': mask_str_generator,
            'foreign_key': choice_from_foreign_table_column_stab,
        },
        'default': rand_str_generator,
    },
    'float': {
        'generator_type_to_gen': {
            'random': rand_float_generator,
            'range': rand_float_generator,
            'choice': rand_choice_generator,
            'foreign_key': choice_from_foreign_table_column_stab,
        },
        'default': rand_float_generator,
    },
    'timestamp': {
        'generator_type_to_gen': {
            'random': rand_timestamp_generator,
            'range': rand_timestamp_generator,
            'choice': rand_choice_generator,
            'foreign_key': choice_from_foreign_table_column_stab,
        },
        'default': rand_timestamp_generator,
    },
    'date': {
        'generator_type_to_gen': {
            'random': rand_date_generator,
            'range': rand_date_generator,
            'choice': rand_choice_generator,
            'foreign_key': choice_from_foreign_table_column_stab,
        },
        'default': rand_date_generator
    }
}


class NeedTableException(RuntimeError):
    pass


class DBGenerator:
    def __init__(self, spark, db_description, override_conf=None):
        self.db_description = db_description
        self.override_conf = override_conf if override_conf else {}
        self.spark = spark
        self._foreign_keys_samples = {}

    def generate_random_rows(
            self,
            input_class,
            table_name: str,
            count: int,
            columns_config: Dict,
            columns_override_conf: Dict,
    ):
        key_to_generator = {}
        secondary_use_info = {
            rec['primary_keys']['table_name']: rec for rec in self.db_description['join_keys'].values()
            if [rec2 for rec2 in rec['secondary_use'] if rec2['table_name'] == table_name]
        }
        primary_use_info = [
            rec for rec in self.db_description['join_keys'].values()
            if rec['primary_keys']['table_name'] == table_name
        ]

        for key, key_class in input_class.__annotations__.items():
            if key_class == int:
                gen_map = GENERATOR_MAP['int']
            elif key_class == str:
                gen_map = GENERATOR_MAP['str']
            elif key_class == float:
                gen_map = GENERATOR_MAP['float']
            elif key_class == TimeStamp:
                gen_map = GENERATOR_MAP['timestamp']
            elif key_class == date:
                gen_map = GENERATOR_MAP['date']
            else:
                raise NotImplementedError(f'No generator for {key_class} for {key} or {input_class}')

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
            rec = input_class(
                **{
                    key: next(gen) for key, gen in key_to_generator.items()
                }
            )
            if secondary_use_info:
                for from_table_name, use_info in secondary_use_info.items():
                    if from_table_name not in self._foreign_keys_samples:
                        raise NeedTableException
                    for reference in use_info['secondary_use']:
                        if reference['table_name'] != table_name:
                            continue
                        template_row = choice(self._foreign_keys_samples[from_table_name])
                        for key, template_key in zip(
                                reference['column_names'],
                                use_info['primary_keys']['column_names'],
                        ):
                            setattr(rec, key, getattr(template_row, template_key))
            if primary_use_info:
                self._foreign_keys_samples.setdefault(table_name, [])
                self._foreign_keys_samples[table_name].append(rec)
            yield rec

    def generate_database(self):
        processed_tables = set()
        result_path_info = {}
        while len(processed_tables) != len(self.db_description['tables']):
            for table_class, table_config in self.db_description['tables'].items():
                table_name = table_config['table_name']
                if table_name in processed_tables:
                    continue

                table_override_conf = self.override_conf.get(table_config['table_name'], {})
                try:
                    df = self.spark.createDataFrame(
                        self.generate_random_rows(
                            table_class,
                            table_name=table_name,
                            count=(table_override_conf.get('count') or table_config['count']),
                            columns_config=table_config['columns'],
                            columns_override_conf=table_override_conf.get('columns', {})
                        )
                    )
                except NeedTableException as e:
                    logging.warning('skip table %r since %r', table_name, e)
                    continue

                df.show()
                res_filename = f"output/{table_name}.parquet"
                try:
                    shutil.rmtree(res_filename)
                except FileNotFoundError:
                    pass
                df.write.parquet(res_filename)
                result_path_info[table_name] = res_filename
                processed_tables.add(table_name)
        return result_path_info
