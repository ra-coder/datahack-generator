from datetime import date
from dataclasses import dataclass


@dataclass
class Schedule:
    id: int
    user_id: int
    group_id: int
    memory_used: float
    label2: str
    label2_new: str
    user_birthday: date


schedule_default_config = {
    'table_name': 'schedule',
    'count': 70,
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
        'user_id': {
            'value_type': 'int',
            'generator_type': 'foreign_key',
            'params': {
                'table_name': 'user',
                'column_name': 'id',
            },
        },
        'user_birthday': {
            'value_type': 'date',
            'generator_type': 'foreign_key',
            'params': {
                'table_name': 'user',
                'column_name': 'birthday',
            },
        },
        'label2': {
            'value_type': 'str',
            'generator_type': 'foreign_key',
            'params': {
                'table_name': 'user',
                'column_name': 'label2',
            },
        },
        'label2_new': {
            'value_type': 'str',
            'generator_type': 'foreign_key',
            'params': {
                'table_name': 'user',
                'column_name': 'label2',
            },
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
    }
}
