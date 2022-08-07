from datetime import datetime, timedelta

from faker import Faker
import arrow


def rand_date_generator(from_value=None, to_value=None, seed=None):
    if from_value:
        from_value = arrow.get(from_value).datetime
    if to_value:
        to_value = arrow.get(to_value).datetime

    if from_value is None and to_value is None:
        to_value = datetime.utcnow()

    if to_value is None:
        to_value = from_value + timedelta(days=365)

    if from_value is None:
        from_value = to_value - timedelta(days=365)

    fake = Faker()
    if seed:
        Faker.seed(seed)
    while True:
        yield fake.date_between_dates(from_value, to_value)
