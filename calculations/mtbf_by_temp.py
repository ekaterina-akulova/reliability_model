from calculations.reliability_indicators import const_failure_rate, mtbf_minute, failure_rate_minute, calculate_by_temp
import pandas as pd
import math


def get_models(df):
    models = []
    for model in df.index.get_level_values('model'):
        models.append(model)
    return models


def bernoulli(p, n, pred_q, pred_p):
    m = 1
    q = (1 - p)
    P = (math.factorial(n) / (math.factorial(m) * math.factorial(n))) * ((((p * pred_p) ** m)) * ((q * pred_q) ** (n - m)))
    return P, p, q


def calculate_mtbf(ts, df_temp):
    values = []
    for index, row in ts.iterrows():
        mask = (df_temp['temp'] == ts.temp[index])
        value = df_temp[mask].values
        # values.append(value[0, 1])
        i = index + 1
        if index == 0:
            ts.loc[index, 'temp_mtbf'] = value[0, 1]
            ts.loc[index, 'mtbf'] = value[0, 1]
            pred_p = value[0, 1] ** 1
            pred_q = (1 - value[0, 1]) ** (i - 1)
        else:
            ts.loc[index, 'temp_mtbf'] = value[0, 1]
            P, pred_p, pred_q = bernoulli(value[0, 1], i, pred_q, pred_p)
            ts.loc[index, 'mtbf'] = P
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
    return mtbf_minutes_25, mtbf_minutes_40, fr_min_25, fr_min_40


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
