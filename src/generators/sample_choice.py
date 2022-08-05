from random import choice
from typing import List


def rand_sample_generator(choices: List):
    while True:
        yield choice(choices)
