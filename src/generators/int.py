from random import randint
from faker import Faker


def rand_int_generator(from_value=0, to_value=100500):
    while True:
        yield randint(from_value, to_value)


def mask_int_generator(mask="##", seed=None) -> int:
    fake = Faker()
    if seed:
        Faker.seed(seed)
    while True:
        yield int(fake.numerify(mask))
