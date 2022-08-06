from typing import Dict

from database.types import TimeStamp
from .float_numbers import rand_float_generator
from .integet import mask_int_generator, rand_int_generator
from .sample_choice import rand_sample_generator
from .string import mask_str_generator, rand_str_generator
from .timestamp import rand_timestamp_generator

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
        yield input_class(
            **{
                key: next(gen) for key, gen in key_to_generator.items()
            }
        )
