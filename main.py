from calculations.mtbf_by_temp import get_models, temperature_mtbf, get_indicators, calculate_mean, find_MTBF
from generate_ts.generate import generate_ts
from generate_ts.init_dataset import get_dataset
import matplotlib.pyplot as plt

from model.train_model import polynomial


def plot(df):
    x = df.temp
    y = df.mtbf
    fig, ax = plt.subplots()
    ax.scatter(x, y, c='deeppink')
    ax.set_facecolor('black')
    ax.set_title('mtbf by temp')
    fig.show()


def main():
    df_orig = get_dataset()
    ts = generate_ts()
    models = get_models(df_orig)
    mtbf_25, mtbf_40, fr_25, fr_40 = get_indicators(df_orig, models, 0)
    df_temp = temperature_mtbf(5, 45, mtbf_25, mtbf_40)
    # plot(df_temp)
    # mtbf_ts = calculate_mean(ts, df_temp, 10)
    MTBF = find_MTBF(26, mtbf_40, mtbf_25)
    print(MTBF)
    # print(mtbf_ts)
    # mtbf_ts['rolling_window'].plot()
    # mtbf_ts['mean_all'].plot()
    # polynomial(mtbf_ts, 5)



main()
