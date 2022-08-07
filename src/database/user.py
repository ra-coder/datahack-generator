from datetime import date
from dataclasses import dataclass

from .types import TimeStamp


@dataclass
class User:
    id: int
    name: str
    group_id: int
    label: int
    label2: str
    created_at: TimeStamp
    birthday: date


user_default_config = {
    'table_name': 'user',
    'count': 5,
    'columns': {
        'id': {
            'value_type': 'int',
            'generator_type': 'range',
            'params':
                {
                    'from_value': 0,
                    'to_value': 12345,
                }
        },
        'name': {
            'value_type': 'str',
            'generator_type': 'random',
        },
        'created_at': {
            'value_type': 'timestamp',
            'generator_type': 'random',
        },
        'group_id': {
            'value_type': 'int',
            'generator_type': 'choice',
            'params':
                {
                    'choices': [1, 2, 3, 4, 5],
                }
        },
        'label': {
            'value_type': 'int',
            'generator_type': 'mask',
            'params':
                {
                    'mask': '#00#',
                }
        },
        'label2': {
            'value_type': 'str',
            'generator_type': 'mask',
            'params':
                {
                    'mask': 'label-###',
                }
        },
        'birthday': {
            'value_type': 'date',
            'generator_type': 'range',
            'params': {
                'from_value': '1950-01-01',
                'to_value': '2020-01-01',
            }
        },
    }
}
