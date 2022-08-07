from random import choice
from typing import List


def rand_choice_generator(choices: List):
    while True:
        yield choice(choices)


def choice_from_foreign_table_column_stab(**_kwargs):
    while True:
        yield None
