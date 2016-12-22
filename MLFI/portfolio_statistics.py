import numpy as np
import pandas as pd

from bollinger import get_data


def statistics():
    dates = pd.date_range('2016-01-01', '2016-12-01')
    symbols = ['SPY', 'AMD', 'GOOG', 'XOM']

    df = get_data(dates, symbols)

    allocations = [.5, .2, .2, .1]

    normalized = df / df.ix[0, :]
    allocated = normalized * allocations
    capital = 1000000
    position_values = allocated * capital

    portfolio_value = position_values.sum(axis=1)

    daily_port_returns = portfolio_value / portfolio_value.shift(1) - 1
    daily_port_returns = daily_port_returns[1:]

    cumulative_return = portfolio_value[-1] - portfolio_value[0]

    average_daily_return = daily_port_returns.mean()
    std_dev = daily_port_returns.std()

    print 'You started with $', capital, \
        'and ended with $', portfolio_value[-1], \
        'for a profit of $', cumulative_return, '\n'
    for symbol in symbols:
        print 'You made $', position_values.ix[-1, symbol] - position_values.ix[0, symbol], ' on ', symbol
    print
    print 'Average daily return: ', average_daily_return
    print 'Std deviation: ', std_dev

    sharpe_ratio = average_daily_return / std_dev
    annualized_sr = np.sqrt(252) * sharpe_ratio

    print 'Sharpe ratio: ', sharpe_ratio
    print 'Annualized Sharpe Ratio: ', annualized_sr


if __name__ == '__main__':
    statistics()
