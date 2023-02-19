import datetime
import pandas as pd
import random


def generate_date(start, l, num_min):
    list_date = []
    current = start
    for i in range(0, l):
        curr = current + datetime.timedelta(minutes=num_min)
        list_date.append(curr)
        current = curr
        l-=1
    return list_date


def generate_temperature(length, start, end):
    list_temp = []
    for i in range(0, length):
        if i < (1/4 * length):
            list_temp.append(random.randint(start + 10, end - 10))
        elif (1/2 * length) > i >= (1/4 * length):
            list_temp.append(random.randint(start + 30, end - 5))
        elif (1/2 * length) <= i < length:
            list_temp.append(random.randint(start, end - 3))
    return list_temp


def generate_ts():
    ts = pd.DataFrame(columns=['time', 'temp'])
    start_date = datetime.datetime(2023, 1, 1, 0, 0)
    ts['time'] = generate_date(start_date, 10080, 1)
    ts['temp'] = generate_temperature(10080, 5, 45)
    return ts




