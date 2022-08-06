from datetime import datetime, timedelta
from random import randint


def rand_timestamp_generator(from_value=None, to_value=None):
    if from_value is None and to_value is None:
        from_value = int((datetime.utcnow() - timedelta(days=365)).timestamp())

    if to_value is None:
        to_value = from_value + timedelta(days=365).total_seconds()

    if from_value is None:
        from_value = to_value - timedelta(days=365).total_seconds()

    while True:
        yield randint(from_value, to_value)
