from dataclasses import dataclass


@dataclass
class User:
    id: int
    name: str
    group_id: int
    memory_used: float


user_default_config = {
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
    }
}
