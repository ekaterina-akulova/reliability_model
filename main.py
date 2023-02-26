from calculations.mtbf_by_temp import get_models, temperature_mtbf, get_indicators, calculate_mean, find_MTBF, \
    calculate_mtbf
from generate_ts.generate import generate_ts, generate_device_work
from generate_ts.init_dataset import get_dataset
import matplotlib.pyplot as plt
import math
import numpy as np
from model.train_model import polynomial



def plot(df):
    x = df.temp
    y = df.mtbf
    fig, ax = plt.subplots()
    ax.scatter(x, y, c='deeppink')
    ax.set_facecolor('black')
    ax.set_title('mtbf by temp')
    fig.show()


def dd(ts):
    delta_t = np.diff(ts['temp'])
    if np.all(delta_t > 0):
        print('Температура во временном ряде увеличивается')
    elif np.all(delta_t < 0):
        print('Температура во временном ряде уменьшается')
    else:
        print('Температура во временном ряде изменяется непостоянно')


def main():
    df_orig = get_dataset()
    ts = generate_ts()
    models = get_models(df_orig)
    mtbf_25, mtbf_40, fr_25, fr_40 = get_indicators(df_orig, models, 0)
    df_temp = temperature_mtbf(5, 45, mtbf_25, mtbf_40)
    device_work = generate_device_work(df_temp)
    # plot(df_temp)
    # ts['temp'].plot()
    df_temp = calculate_mtbf(ts, df_temp)
    # mtbf_ts = calculate_mean(ts, df_temp, 10)

    # MTBF = find_MTBF(26, mtbf_40, mtbf_25)
    # print(MTBF)

    # dd(ts)



main()
