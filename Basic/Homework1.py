import datetime as date

import QSTK.qstkutil.DataAccess as dataAccess
import QSTK.qstkutil.qsdateutil as dateUtil
import QSTK.qstkutil.tsutil as tsUtil
import numpy as numpy


def simulate(begindate, enddate, tickers, weightings):
    dt_delta = date.timedelta(hours=16)
    ldt_timestamps = dateUtil.getNYSEdays(begindate, enddate, dt_delta)

    ls_keys = ['close']
    c_dataobj = dataAccess.DataAccess('Yahoo')
    ldf_data = c_dataobj.get_data(ldt_timestamps, tickers, ls_keys)
    d_data = dict(zip(ls_keys, ldf_data))

    # Grab the closing values of every stock
    temp = d_data['close'].values.copy()
    # Normalize those values with respect to the initial value
    d_normal = temp / temp[0, :]
    alloc = numpy.array(weightings).reshape(4, 1)
    # Multiply the normalized daily changes by the allocation
    # This gives us an array reflecting the amount allocated to each stock
    portVal = numpy.dot(d_normal, alloc)

    dailyVal = portVal.copy()
    tsUtil.returnize0(dailyVal)

    daily_ret = numpy.mean(dailyVal)
    volatility = numpy.std(dailyVal)
    sharpe = numpy.sqrt(252) * daily_ret / volatility
    total_returns = portVal[portVal.shape[0] - 1][0]

    return volatility, daily_ret, sharpe, total_returns


def best_portfolio(start, end, tickers, allocations):
    best_sharpe = -100.0
    best_vol = 0.0
    best_daily_ret = 0.0
    best_cum_ret = 0.0
    best_allocations = []
    for i in range(0, 10, 1):
        for j in range(0, 10, 1):
            for k in range(0, 10, 1):
                for l in range(0, 10, 1):
                    if i + j + k + l == 10:
                        weightings = [float(i) / 10, float(j) / 10, float(k) / 10, float(l) / 10]
                        vol, daily_ret, sharpe, cum_ret = simulate(start, end, tickers, weightings)
                        if sharpe > best_sharpe:
                            best_sharpe = sharpe
                            best_vol = vol
                            best_daily_ret = daily_ret
                            best_cum_ret = cum_ret
                            best_allocations = weightings
    print "Start Date: %s" % start
    print "End Date: %s" % end
    print "Symbols: %s" % tickers
    print "Optimal Allocations: %s" % best_allocations
    print "Sharpe Ratio: %s" % best_sharpe
    print "Volatility (stdev of daily returns): %s" % best_vol
    print "Average Daily Return: %s" % best_daily_ret
    print "Cumulative Return: %s" % best_cum_ret


def main():
    start = date.datetime(2011, 1, 1)
    end = date.datetime(2011, 12, 31)
    best_portfolio(start, end, ['AAPL', 'GLD', 'GOOG', 'XOM'], [0.4, 0.4, 0.0, 0.2])


if __name__ == '__main__':
    main()
