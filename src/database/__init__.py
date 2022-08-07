from .user import User, user_default_config
from .user_bio import UserBio, user_bio_default_config
from .company import Company, company_default_config
from .category import Category, category_default_config
from .schedule import Schedule, schedule_default_config

JOIN_KEYS = {
    'user_info': {
        'primary_keys': {
            'table_name': 'user',
            'column_names': ['id', 'birthday', 'label2'],
        },
        'secondary_use': [
            {
                'table_name': 'schedule',
                'column_names': ['user_id', 'user_birthday', 'label2'],
            }
        ],
    },
    'user_id': {
        'primary_keys': {
            'table_name': 'user',
            'column_names': ['id'],
        },
        'secondary_use': [
            {
                'table_name': 'user_bio',
                'column_names': ['user_id'],
            }
        ],
    }

}

DB_DESCRIPTION = {
    'join_keys': JOIN_KEYS,
    'tables': {
        User: user_default_config,
        UserBio: user_bio_default_config,
        Company: company_default_config,
        Category: category_default_config,
        Schedule: schedule_default_config
    },
}
