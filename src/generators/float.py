import random


def rand_float_generator(from_value=0.1, to_value=32.0):
    while True:
        yield random.uniform(from_value, to_value)


def rand_timestamp_generator(from_value=1625389452.157246, to_value=1825404472.352341):
    while True:
        yield random.uniform(from_value, to_value)
