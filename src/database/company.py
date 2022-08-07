from datetime import date
from dataclasses import dataclass


@dataclass
class Company:
    id: int
    address: str
    name: str
    slag: str
    group_id: int
    owner_id: int
    category_id: int
    created_at: date


company_default_config = {
    'table_name': 'company',
    'count': 11000,
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
        'address': {
            'value_type': 'str',
            'generator_type': 'random',
            'params':
                {
                    'min_chars': 5,
                    'max_chars': 100,
                }
        },
        'name': {
            'value_type': 'str',
            'generator_type': 'mask',
            'params':
                {
                    'mask': '###### Inc.'
                }
        },
        'slag': {
            'value_type': 'str',
            'generator_type': 'random',
            'params':
                {
                    'min_chars': 5,
                    'max_chars': 5,
                }
        },
        'group_id': {
            'value_type': 'int',
            'generator_type': 'choice',
            'params':
                {
                    'choices': [1, 2, 3, 4, 5],
                }
        },
        'category_id': {
            'value_type': 'int',
            'generator_type': 'foreign_key',
            'params': {
                'table_name': 'category',
                'column_name': 'id',
            },
        },
        'owner_id': {
            'value_type': 'int',
            'generator_type': 'foreign_key',
            'params': {
                'table_name': 'user',
                'column_name': 'id',
            },
        },
        'created_at': {
            'value_type': 'date',
            'generator_type': 'range',
            'params': {
                'from_value': '2010-01-01',
                'to_value': '2030-01-01',
            }
        },
    }
}
