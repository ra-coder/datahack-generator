from faker import Faker


fake = Faker()


def rand_str_generator():
    while True:
        yield fake.name()
