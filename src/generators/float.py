import random


def rand_float_generator(from_value=0, to_value=1):
    while True:
        yield random.uniform(from_value, to_value)
