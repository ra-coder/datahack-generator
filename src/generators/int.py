from random import randint
from faker import Faker


def rand_int_generator(from_value=0, to_value=100500):
    while True:
        yield randint(from_value, to_value)


def rand_int_generator_faker(from_value=0, to_value=100500, seed=1234):
    fake = Faker()
    Faker.seed(seed)
    while True:
        yield fake.bothify(text=f'{randint(from_value, to_value)} #####')
