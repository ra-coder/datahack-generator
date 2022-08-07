from datetime import date
from dataclasses import dataclass


@dataclass
class Company:
    id: int
    address: str
    name: str
    group_id: int
    memory_used: float
    created_at: date


company_default_config = {
    'table_name': 'company',
    'count': 20,
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
        },
        'name': {
            'value_type': 'str',
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
        'memory_used': {
            'value_type': 'float',
            'generator_type': 'range',
            'params':
                {
                    'from_value': 0.0,
                    'to_value': 32.0,
                }
        },
        'created_at': {
            'value_type': 'datetime',
            'generator_type': 'range',
            'params': {
                'from_value': '2010-01-01',
                'to_value': '2030-01-01',
            }
        },
    }
}