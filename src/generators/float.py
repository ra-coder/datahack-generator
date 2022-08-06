import random


def rand_float_generator(from_value=0.1, to_value=32.0):
    while True:
        yield random.uniform(from_value, to_value)
