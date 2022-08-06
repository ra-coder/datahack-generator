from faker import Faker


def rand_str_generator():
    fake = Faker()
    while True:
        yield fake.pystr(min_chars=1, max_chars=20)
