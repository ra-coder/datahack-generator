from faker import Faker


def rand_str_generator():
    fake = Faker()
    while True:
        yield fake.pystr(min_chars=1, max_chars=20)


def mask_str_generator(mask="##", seed=None) -> int:
    mask = "?".join(mask.split("#"))
    fake = Faker()
    if seed:
        Faker.seed(seed)
    while True:
        yield fake.lexify(mask)
