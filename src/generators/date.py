import datetime

# Date generator with timedelta in seconds
def date_generator(dt = datetime.datetime(2010, 12, 1), 
                   end = datetime.datetime(2010, 12, 30, 23, 59, 59),
                   step = datetime.timedelta(seconds=5)):
    while dt < end:
        yield dt.strftime('%Y-%m-%d %H:%M:%S')
        dt += step