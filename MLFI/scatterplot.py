from histogram import compute_daily_returns

import pandas as pd
import matplotlib.pyplot as plt

from bollinger import get_data, plot_data

import numpy as np


def scatter():
    dates = pd.date_range('2009-01-01', '2012-12-31')
    symbols = ['SPY', 'AMD', 'XOM', 'GLD']
    df = get_data(dates, symbols)
    # plot_data(df)

    daily_returns = compute_daily_returns(df)
    # plot_data(daily_returns, title='Daily returns', ylabel='Daily returns')

    daily_returns.plot(kind='scatter', x='SPY', y='XOM')
    beta_XOM, alphaXOM = np.polyfit(daily_returns['SPY'], daily_returns['XOM'], 1)
    print "XOM beta: ", beta_XOM
    print "XOM alpha: ", alphaXOM

    plt.plot(daily_returns['SPY'], beta_XOM * daily_returns['SPY'] + alphaXOM, '-', color='r')
    plt.show()

    daily_returns.plot(kind='scatter', x='SPY', y='GLD')
    beta_GLD, alpha_GLD = np.polyfit(daily_returns['SPY'], daily_returns['GLD'], 1)
    print "GLD beta: ", beta_GLD
    print "GLD alpha: ", alpha_GLD
    plt.plot(daily_returns['SPY'], beta_GLD * daily_returns['SPY'] + alpha_GLD, '-', color='r')
    plt.show()

    print daily_returns.corr(method='pearson')


if __name__ == '__main__':
    scatter()
