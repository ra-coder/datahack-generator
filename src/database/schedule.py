from dataclasses import dataclass


@dataclass
class Schedule:
    id: int
    address: str
    name: str
    group_id: int
    memory_used: float
    timestamp: float


schedule_default_config = {
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
    'timestamp': {
        'value_type': 'float',
        'generator_type': 'range',
        'params':
            {
                'from_value': 1625389452.157246,
                'to_value': 1825404472.352341,
            }
    }
}