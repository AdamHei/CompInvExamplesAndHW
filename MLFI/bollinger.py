import os

import matplotlib.pyplot as plt
import pandas as pd


def symbol_to_path(symbol, bas_dir="../Historical_Data"):
    return os.path.join(bas_dir, "{}.csv".format(str(symbol)))


def get_data(dates, symbols):
    df = pd.DataFrame(index=dates)

    for symbol in symbols:
        df_temp = pd.read_csv(symbol_to_path(symbol), index_col='Date', parse_dates=True,
                              usecols=['Date', 'Adj Close'], na_values=['nan'])
        df_temp = df_temp.rename(columns={'Adj Close': symbol})
        df = df.join(df_temp)
        if symbol == 'SPY':
            df = df.dropna(subset=['SPY'])

    return df


def plot_data(df, title='Stock Prices', ylabel='Price'):
    ax = df.plot(title=title, fontsize=12)
    ax.set_xlabel('Date')
    ax.set_ylabel(ylabel)
    plt.show()


def get_rolling_mean(values, window):
    return values.rolling(window=window, center=False).mean()
    # return pd.rolling_mean(values, window=window)


def get_rolling_std(values, window):
    return values.rolling(window=window, center=False).std()
    # return pd.rolling_std(values, window=window)


def get_bollinger_bands(roll_mean, roll_std):
    upper_band = 2 * roll_std + roll_mean
    lower_band = roll_mean - 2 * roll_std
    return upper_band, lower_band


def test_run():
    dates = pd.date_range('2016-01-01', '2016-12-19')
    df = get_data(dates, ['AMD'])

    df['AMD'].ffill(inplace=True)

    roll_m = get_rolling_mean(df['AMD'], 20)

    roll_std = get_rolling_std(df['AMD'], 20)

    upper, lower = get_bollinger_bands(roll_m, roll_std)

    ax = df['AMD'].plot(title="Bollinger Bands", label="AMD")
    roll_m.plot(label='Rolling mean', ax=ax)
    upper.plot(label='upper band', ax=ax)
    lower.plot(label='lower band', ax=ax)

    ax.set_xlabel('Date')
    ax.set_ylabel('Price')
    ax.legend(loc='upper left')

    plt.show()


if __name__ == "__main__":
    test_run()
