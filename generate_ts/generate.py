import datetime
import pandas as pd
import random
import numpy as np


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


def generate_device_work(df):
    temperature_range = list(df['temp']) # диапазон температур
    failure_probability = list(df['prob_fail']) # вероятность отказа
    temperature_failure_dict = dict(zip(temperature_range, failure_probability))
    num_simulations = 1000
    results = [[]]
    n = 0
    result = 1
    temperature = random.choice(temperature_range)  # выбираем случайную температуру
    failure_prob = temperature_failure_dict[temperature]  # получаем вероятность отказа
    for i in range(num_simulations):
        if result != 0:
            result = np.random.choice([0, 1], p=[failure_prob, 1-failure_prob])
            results[n].append((temperature, result))
        else:
            temperature = random.choice(temperature_range) # выбираем случайную температуру
            failure_prob = temperature_failure_dict[temperature] # получаем вероятность отказа
            n += 1
    return results

# def generate_device_work1(df, temp_list): # диапазон температур
#     failure_probability = list(df['afr'])  # вероятность отказа
#     temperature_failure_dict = dict(zip(temp_list, failure_probability))
#     num_simulations = 1000
#     results = [[]]
#     n = 0
#     result = 1
#     for temp in random.choice(temp_list):
