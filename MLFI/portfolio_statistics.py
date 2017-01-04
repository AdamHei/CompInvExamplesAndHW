import numpy as np
import pandas as pd

from bollinger import get_data


def get_portfolio_value(prices, allocations, start_val=1):
    df = prices / prices.ix[0]
    df *= allocations
    df *= start_val
    return df.sum(axis=1)


def get_portfolio_stats(port_val, daily_rf=0, samples_per_year=252):
    cumulative_return = port_val[-1] / port_val[0] - 1

    daily_returns = port_val.copy()
    daily_returns = daily_returns / daily_returns.shift(1) - 1
    daily_returns.ix[0, 0] = 0

    average_daily_ret = daily_returns.mean()
    std_daily_ret = daily_returns.std()

    sharpe_ratio = ((daily_returns - daily_rf).mean() / std_daily_ret) * np.sqrt(samples_per_year)

    return cumulative_return, average_daily_ret, std_daily_ret, sharpe_ratio


def assess_portfolio(start_date, end_date, symbols, allocations, start_val=1):
    dates = pd.date_range(start_date, end_date)
    all_prices = get_data(dates, symbols)
    prices = all_prices[symbols]

    port_val = get_portfolio_value(prices, allocations, start_val)

    cum_ret, avg_daily_ret, std_daily_ret, sharpe_ratio = get_portfolio_stats(port_val)

    print 'Start Date: ', start_date
    print 'End Date: ', end_date
    print 'Symbols: ', symbols
    print 'Allocations: ', allocations
    print 'Sharpe Ratio: ', sharpe_ratio
    print 'Volatility: ', std_daily_ret
    print 'Average Daily Return: ', avg_daily_ret
    print 'Cumulative return: ', cum_ret


def statistics():
    dates = pd.date_range('2016-01-01', '2016-12-01')
    symbols = ['SPY', 'AMD', 'GOOG', 'XOM']

    df = get_data(dates, symbols)

    allocations = [.5, .2, .2, .1]
    capital = 1000000

    portfolio_value = get_portfolio_value(df, allocations, capital)

    daily_port_returns = portfolio_value / portfolio_value.shift(1) - 1
    daily_port_returns = daily_port_returns[1:]

    cumulative_return = portfolio_value[-1] - portfolio_value[0]

    average_daily_return = daily_port_returns.mean()
    std_dev = daily_port_returns.std()

    print 'You started with $', capital, \
        'and ended with $', portfolio_value[-1], \
        'for a profit of $', cumulative_return, '\n'
    print 'Average daily return: ', average_daily_return
    print 'Std deviation: ', std_dev

    sharpe_ratio = average_daily_return / std_dev
    annualized_sr = np.sqrt(252) * sharpe_ratio

    print 'Sharpe ratio: ', sharpe_ratio
    print 'Annualized Sharpe Ratio: ', annualized_sr


if __name__ == '__main__':
    assess_portfolio('2008-01-01', '2010-12-31', ['SPY', 'AMD', 'GOOG', 'XOM'], [.5, .2, .2, .1], start_val=1000000)
