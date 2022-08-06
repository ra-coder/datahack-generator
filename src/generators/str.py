from faker import Faker


fake = Faker()


def rand_str_generator():
    while True:
        yield fake.pystr(min_chars=1, max_chars=20)
