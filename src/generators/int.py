from random import randint


def rand_int_generator(from_value=0, to_value=100500):
    while True:
        yield randint(from_value, to_value)
