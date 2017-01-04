import numpy as np
import pandas as pd
import scipy.optimize as spo

from portfolio_statistics import get_portfolio_value, get_portfolio_stats
from util_fns import get_data, plot_data


def find_optimal_allocations(prices):
    # Initial guess is equal weighing to all
    initial_guess = 1.0 / prices.shape[1]
    function_guess = [initial_guess] * prices.shape[1]
    # Can never have allocation outside 0 and 1
    bounds = [[0, 1] for _ in prices.columns]

    constraints = ({'type': 'eq', 'fun': lambda function_guess: 1.0 - np.sum(function_guess)})
    result = spo.minimize(opt_alloc_error, function_guess, args=(prices,), method='SLSQP', bounds=bounds,
                          constraints=constraints)
    return result.x


def opt_alloc_error(allocations, prices):
    """Our minimized error is actually the negative sharpe ratio, thus we are maximizing the sharpe ratio"""
    portfolio_value = get_portfolio_value(prices, allocations, 1)
    cum_ret, avg_daily_ret, std_daily_ret, sharpe_ratio = get_portfolio_stats(portfolio_value)
    error = sharpe_ratio * -1
    return error


def optimize_portfolio(sd, ed, symbols, gen_plot):
    dates = pd.date_range(sd, ed)
    all_prices = get_data(dates, symbols)

    prices = all_prices[symbols]
    prices_SPY = all_prices['SPY']

    allocations = find_optimal_allocations(prices)
    allocations /= np.sum(allocations)  # Normalizing

    portfolio_value = get_portfolio_value(prices, allocations)

    cum_ret, avg_daily_ret, std_daily_ret, sharpe_ratio = get_portfolio_stats(portfolio_value)

    print "Start Date:", sd
    print "End Date:", ed
    print "Symbols:", symbols
    print "Optimal allocations:", allocations
    print "Sharpe Ratio:", sharpe_ratio
    print "Volatility (stdev of daily returns):", std_daily_ret
    print "Average Daily Return:", avg_daily_ret
    print "Cumulative Return:", cum_ret

    normalized_SPY = prices_SPY / prices_SPY.ix[0, :]
    df_temp = pd.concat([portfolio_value, normalized_SPY], keys=['Portfolio', 'SPY'], axis=1)
    plot_data(df_temp, title='Daily Portfolio Value and SPY')


def test_run():
    start = '2015-01-01'
    end = '2015-12-01'
    symbols = ['GOOG', 'AAPL', 'AMD', 'XOM', 'SPY']

    optimize_portfolio(start, end, symbols, False)


if __name__ == '__main__':
    test_run()
