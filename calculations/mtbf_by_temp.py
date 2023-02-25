import numpy as np
from calculations.reliability_indicators import const_failure_rate, mtbf_minute, failure_rate_minute, calculate_by_temp, \
    probability_without_fail
import pandas as pd
import math


def get_models(df):
    models = []
    for model in df.index.get_level_values('model'):
        models.append(model)
    return models


def bernoulli1(fr, list_pred_q, pred_p):
    # p_t = p(t)
    p_t = 1 - probability_without_fail(fr, 1)
    if (list_pred_q == []):
        return p_t
    else:
        pred_prob_q = math.prod(list_pred_q)
        return (pred_prob_q * p_t) + pred_p


def bernoulli(p, n, pred_q, pred_p):
    m = 1
    q = (1 - p)
    prob_fail = p * pred_p
    prob_work = q * pred_q
    # P2 = pred_p * prob_work + p * prob_fail
    P = n * (prob_fail * prob_work)
    return prob_work, prob_fail, prob_work


def indicator_change(temp1, value1, temp2, value2):
    # a = value1/temp1
    # b = temp2/temp1
    # c = value2/b
    # r = c ** a
    res = value2/(temp2/temp1)
    return res


def probability_fail(n, fr, last_prob_fail, last_prob_work):
    m = 1
    prob_work = probability_without_fail(fr, 1)
    prob_work = prob_work * last_prob_work
    prob_fail = 1 - prob_work
    # prob_wrk_1 = 1 - prob_fail
    return prob_work, prob_fail, prob_work


def calculate_mtbf(ts, df_temp):
    values = []
    for index, row in ts.iterrows():
        mask = (df_temp['temp'] == ts.temp[index])
        value = df_temp[mask].values
        list_q = []
        values.append(value[0])
        i = index + 1
        if index == 0:
            ts.loc[index, 'temp_afr'] = value[0, 2]
            # ts.loc[index, 'mtbf'] = value[0, 1]
            pred_p = value[0, 2]
            pred_q = (1 - pred_p)
            list_q += [pred_q]
            pred_prob_work = probability_without_fail(value[0, 2], 1)
            pred_prob_fail = 1 - pred_prob_work
            ts.loc[index, 'prob'] = pred_prob_work
            # ts.loc[index, 'prob_fail'] = pred_prob_fail
        else:
            ts.loc[index, 'temp_afr'] = value[0, 2]
            P = bernoulli1(value[0, 2], list_q, pred_p)
            q = 1 - value[0, 2]
            pred_p = value[0, 2]
            ts.loc[index, 'prob1'] = P
            list_q += [q]
            P1, pred_p, pred_q = bernoulli(value[0, 2], i, pred_q, pred_p)
            ts.loc[index, 'pred_afr'] = indicator_change(values[index - 1][0], values[index - 1][2], values[index][0], values[index][2])
            P, pred_prob_fail, pred_prob_work = probability_fail(i, value[0, 2], pred_prob_fail, pred_prob_work)
            ts.loc[index, 'prob'] = P1
            ts.loc[index, 'prob_work'] = P
            return ts


def find_MTBF(t, MTBF40, MTBF25):
    b = math.log(MTBF40 / MTBF25) / 15
    MTBF = MTBF25 / math.exp(b * 25)
    if t < 10:
        b1 = b * 2
        t1 = 10 - t
        return MTBF * math.exp((b * t) - (t1 * -b1))
    if t < 25:
        b1 = b * 2
        t1 = 25 - t
        return MTBF * math.exp((b * t) - (t1 * -b1))
    if t > 40:
        b1 = b * 2
        t1 = t - 40
        return MTBF * math.exp((b * t) - (t1 * -b1))
    return MTBF * math.exp(b*t)


def get_indicators(df, models, i):
    xs = pd.IndexSlice
    mtbf_25 = df.loc[xs[:, models[i]], 'mtbf_25'].values[0]
    mtbf_40 = df.loc[xs[:, models[i]], 'mtbf_40'].values[0]
    failure_rate_25 = const_failure_rate(mtbf_25)
    failure_rate_40 = const_failure_rate(mtbf_40)
    mtbf_minutes_40 = mtbf_minute(mtbf_40)
    mtbf_minutes_25 = mtbf_minute(mtbf_25)
    fr_min_40 = failure_rate_minute(failure_rate_40)
    fr_min_25 = failure_rate_minute(failure_rate_25)
    return mtbf_25, mtbf_40, fr_min_25, fr_min_40


def temperature_mtbf(range1, range2, mtbf_25, mtbf_40):
    step, step_2 = calculate_by_temp(mtbf_25, mtbf_40, 25, 40, 2)
    df = pd.DataFrame(columns=['temp', 'mtbf'])
    df['temp'] = sorted(range(range1, range2))
    for index, row in df.iterrows():
        if 40 >= df.temp[index] >= 25:
            df.loc[index, 'mtbf'] = ((df.temp[index] - 25) * step) + mtbf_25
        elif 25 > df.temp[index] >= 10:
            df.loc[index, 'mtbf'] = ((25 - df.temp[index]) * step) + mtbf_25
        elif 40 < df.temp[index]:
            df.loc[index, 'mtbf'] = ((df.temp[index] - 40) * step_2) + mtbf_40
        elif 10 > df.temp[index] >= 0:
            df.loc[index, 'mtbf'] = ((10 - df.temp[index]) * step_2) + mtbf_40
        elif 0 > df.temp[index]:
            df.loc[index, 'mtbf'] = ((10 + abs(df.temp[index])) * step_2) + mtbf_40
        df.loc[index, 'afr'] = const_failure_rate(df.loc[index, 'mtbf'])
    return df


def calculate_mean(ts, df_temp, window):
    values = 0
    for index, row in ts.iterrows():
        mask = (df_temp['temp'] == ts.temp[index])
        value = df_temp[mask].values
        values += value[0, 1]
        if index == 0:
            ts.loc[index, 'temp_mtbf'] = value[0, 1]
            ts.loc[index, 'mean_all'] = value[0, 1]
        else:
            i = index + 1
            ts.loc[index, 'temp_mtbf'] = value[0, 1]
            ts.loc[index, 'mean_all'] = (values / i) - 1
            ts['rolling_window'] = ts['temp_mtbf'].rolling(window).mean() - 1
    return ts
