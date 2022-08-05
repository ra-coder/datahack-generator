from random import randint

from database import User
from generators.int import randint_generator
from generators.str import randstr_generator


def generate_random_data_v0(input_class, count: int):
    for _ in range(count):
        raw_data = dict()
        for key, key_class in input_class.__annotations__.items():
            if key_class == int:
                raw_data[key] = randint(0, 1000)
            elif key_class == str:
                raw_data[key] = 'aabs'
        res = input_class(**raw_data)
        yield res


def generate_random_data_v1(input_class, count: int):
    key_to_generator = {}
    for key, key_class in input_class.__annotations__.items():
        if key_class == int:
            key_to_generator[key] = randint_generator()
        elif key_class == str:
            key_to_generator[key] = randstr_generator()

    for _ in range(count):
        yield input_class(
            **{
                key: next(gen) for key, gen in key_to_generator.items()
            }
        )


if __name__ == '__main__':
    for rec in generate_random_data_v1(User, count=3):
        print(rec)
