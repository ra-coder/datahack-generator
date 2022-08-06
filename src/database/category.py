from dataclasses import dataclass


@dataclass
class Category:
    id: int
    name: str
    memory_used: float


category_default_config = {
    'table_name': 'category',
    'count': 50,
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
