import os

import matplotlib.pyplot as plt
import pandas as pd


def symbol_to_path(symbol, bas_dir="C:/Users/Adam/Desktop"):
    return os.path.join(bas_dir, "{}.csv".format(str(symbol)))


def get_data(dates, symbol='amd'):
    df = pd.DataFrame(index=dates)
    df_temp = pd.read_csv(symbol_to_path(symbol), index_col='Date', parse_dates=True,
                          usecols=['Date', 'Adj Close'], na_values=['nan'])
    df_temp = df_temp.rename(columns={'Adj Close': symbol})

    df = df.join(df_temp)
    df = df.dropna()

    return df


def plot_data(df, title='Stock Prices'):
    ax = df.plot(title=title, fontsize=12)
    ax.set_xlabel('Date')
    ax.set_ylabel('Price')
    plt.show()


def get_rolling_mean(values, window):
    return pd.rolling_mean(values, window=window)


def get_rolling_std(values, window):
    return pd.rolling_std(values, window=window)


def get_bollinger_bands(roll_mean, roll_std):
    upper_band = 2 * roll_std + roll_mean
    lower_band = roll_mean - 2 * roll_std
    return upper_band, lower_band


def test_run():
    dates = pd.date_range('1983-12-19', '2016-12-19')
    df = get_data(dates)

    roll_m = get_rolling_mean(df['amd'], 20)

    roll_std = get_rolling_std(df['amd'], 20)

    upper, lower = get_bollinger_bands(roll_m, roll_std)

    ax = df['amd'].plot(title="Bollinger Bands", label="AMD")
    roll_m.plot(label='Rolling mean', ax=ax)
    upper.plot(label='upper band', ax=ax)
    lower.plot(label='lower band', ax=ax)

    ax.set_xlabel('Date')
    ax.set_ylabel('Price')
    ax.legend(loc='upper left')

    print df.max()
    # plt.show()


if __name__ == "__main__":
    test_run()
