import os
import pandas as pd
import matplotlib.pyplot as plt


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
