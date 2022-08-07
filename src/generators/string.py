from faker import Faker
from math import inf


def rand_str_generator(min_chars=1, max_chars=inf):
    fake = Faker()
    while True:
        if max_chars != inf:
            yield fake.pystr(min_chars=min_chars, max_chars=max_chars)
        else:
            # TODO join str with random coin flip for additional call
            yield fake.pystr(min_chars=min_chars, max_chars=100500)


def mask_str_generator(mask="##", seed=None) -> int:
    mask = "?".join(mask.split("#"))
    fake = Faker()
    if seed:
        Faker.seed(seed)
    while True:
        yield fake.lexify(mask)
