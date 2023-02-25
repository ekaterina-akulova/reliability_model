import math


def calculate_by_temp(x1_value, x2_value, x1, x2, k): #x1 = mtbf_min = 25, x2 = mtbf_max = 40,
 #x1_value = mtbf_min(25)_value = 81486982.8, x2_value = mtbf_max(40)_value = 35297175.6
    step_between = x2_value - x1_value
    step = step_between / (x2 - x1)
    step_2 = step * k  #k = 2
    return step, step_2


def const_failure_rate(mtbf): #интенсивность отказов за единицу времени
    return float('{:.4f}'.format(1 / mtbf))


def failure_rate_minute(fail_rate): #интенсивность отказов за минуту
    day_fl = fail_rate/365
    return float('{:.10f}'.format(day_fl / 1440))


def mtbf_minute(mtbf):
    return mtbf * 525960


def reliability(fail_rate, time): #надежность при заданной интенсивности отказов и времени работы
    return float('{:.10f}'.format(math.exp((-1) * fail_rate * time)))


def probability_without_fail(fail_rate, time):
    return float('{:.10f}'.format(math.exp((-1) * fail_rate * time)))


def make_reliability_function(fail_rate): #экспоненциальная функция надежности
    return lambda t: math.exp(-1 * fail_rate * t)


def deduce_reliability_function(time, reliability): #экспоненциальная функция надежности по надежности в определенный момент времени
    failure_rate = math.log(reliability) / time / -1
    return make_reliability_function(failure_rate)


