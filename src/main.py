from random import randint

from database import User


def generate_random_data(input_class, count: int):
    for _ in range(count):
        raw_data = dict()
        for key, key_class in input_class.__annotations__.items():
            if key_class == int:
                raw_data[key] = randint(0, 1000)
            elif key_class == str:
                raw_data[key] = 'aabs'
        res = input_class(**raw_data)
        yield res


if __name__ == '__main__':
    for rec in generate_random_data(User, count=3):
        print(rec)
