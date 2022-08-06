from random import randint
from faker import Faker

fake = Faker()
Faker.seed(0)


def rand_int_generator(from_value=0, to_value=100500):
    while True:
        yield fake.bothify(text=f'{randint(from_value, to_value)} #####')
