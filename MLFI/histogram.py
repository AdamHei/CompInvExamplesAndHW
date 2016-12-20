import pandas as pd
import matplotlib.pyplot as plt

from bollinger import get_data, plot_data


def compute_daily_returns(df):
    daily_returns = df.copy()
    daily_returns[1:] = (df[1:] / df[:-1].values) - 1
    daily_returns.ix[0, :] = 0
    return daily_returns


def driver_method():
    dates = pd.date_range('2009-01-01', '2012-12-31')
    symbols = ['SPY', 'AMD']
    df = get_data(dates, symbols)

    daily_returns = compute_daily_returns(df)
    # plot_data(daily_returns, title='Daily returns', ylabel='Daily returns')

    daily_returns['AMD'].hist(bins=20, label='AMD')
    daily_returns['SPY'].hist(bins=20, label='SPY')
    plt.legend(loc='upper right')
    plt.show()

    mean = daily_returns['SPY'].mean()
    print 'mean: ', mean
    std = daily_returns['SPY'].std()
    print 'std: ', std, '\n'

    # Add mean and either side standard deviations to graph
    plt.axvline(mean, color='r', linestyle='dashed', linewidth=2)
    plt.axvline(std, color='g', linestyle='dashed', linewidth=2)
    plt.axvline(-std, color='g', linestyle='dashed', linewidth=2)
    # plt.show()

    # Kurtosis: how far the tails deviate from Gaussian distro
    # Positive means above; negative below
    print 'Kurtosis values:\n', daily_returns.kurt()


if __name__ == '__main__':
    driver_method()
