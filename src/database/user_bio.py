from dataclasses import dataclass

from .types import TimeStamp


@dataclass
class UserBio:
    user_id: int
    updated_at: TimeStamp
    text: str


user_bio_default_config = {
    'table_name': 'user_bio',
    'count': 300,
    'columns': {
        'user_id': {
            'value_type': 'int',
            'generator_type': 'foreign_key',
            'params': {
                'table_name': 'user',
                'column_name': 'id',
            },
        },
        'created_at': {
            'value_type': 'timestamp',
            'generator_type': 'random',
        },
        'text': {
            'value_type': 'str',
            'generator_type': 'random',
        },
    }
}
