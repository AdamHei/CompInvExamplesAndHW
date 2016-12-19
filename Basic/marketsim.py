import datetime

import QSTK.qstkutil.DataAccess as dataAccess
import QSTK.qstkutil.qsdateutil as dateUtil
import QSTK.qstkutil.tsutil as tsUtil
import numpy as numpy
import csv
import sys
import getopt
import pandas


def get_cash_frame(ldt_timestamps, capital, symbols, trade_data_frame, close_data):

    cash_data_frame = pandas.DataFrame(index=ldt_timestamps, columns=['Cash'])
    cash_data_frame['Cash'][ldt_timestamps[0]] = capital

    order = 0
    temp_symbol = ''
    for sym in symbols:
        if trade_data_frame[sym][ldt_timestamps[0]] != 0:
            order = trade_data_frame[sym][ldt_timestamps[0]]
            temp_symbol = sym
    if len(temp_symbol) > 0:
        cash_data_frame['Cash'][ldt_timestamps[0]] = capital - (order * close_data[0][temp_symbol][ldt_timestamps][0])
    else:
        cash_data_frame['Cash'][ldt_timestamps[0]] = capital

    print cash_data_frame['Cash'][ldt_timestamps[0]]

    for i in range(1, len(ldt_timestamps)):
        order = 0
        temp_symbol = ''
        for sym in symbols:
            if trade_data_frame[sym][ldt_timestamps[i]] != 0:
                order = trade_data_frame[sym][ldt_timestamps[i]]
                temp_symbol = sym
        if len(temp_symbol) > 0:
            cash_data_frame['Cash'][ldt_timestamps[i]] = cash_data_frame['Cash'][ldt_timestamps[i - 1]] - (
                order * close_data[0][temp_symbol][ldt_timestamps][i])
        else:
            cash_data_frame['Cash'][ldt_timestamps[i]] = cash_data_frame['Cash'][ldt_timestamps[i - 1]]

    return cash_data_frame


def main(argv):
    opts, args = getopt.getopt(argv, "")
    capital = int(args[1])
    orders_file = args[2]
    output_file = args[3]

    reader = csv.reader(open(orders_file, 'rU'), delimiter=',')
    dates = []
    symbols = []

    for row in reader:
        date_to_add = datetime.datetime(int(row[0]), int(row[1]), int(row[2]))
        dates.append(date_to_add)

        if row[3] not in symbols:
            symbols.append(row[3])

    start_date = dates[0]
    end_date = dates[len(dates) - 1] + dateUtil.timedelta(days=1)
    ldt_timestamps = dateUtil.getNYSEdays(start_date, end_date, dateUtil.timedelta(hours=16))

    data_obj = dataAccess.DataAccess('Yahoo')
    keys = ['actual_close', 'close']

    close_data = data_obj.get_data(ldt_timestamps, symbols, keys)

    trade_data_frame = pandas.DataFrame(index=ldt_timestamps, columns=symbols)
    trade_data_frame = trade_data_frame.fillna(0)

    reader = csv.reader(open(orders_file, 'rU'), delimiter=',')
    for row in reader:
        date = datetime.datetime(int(row[0]), int(row[1]), int(row[2])) + datetime.timedelta(hours=16)
        symbol = row[3]
        order_type = row[4]
        amount = int(row[5])
        trade_data_frame[symbol][date] = amount if order_type == 'Buy' else (amount * -1)

    cash_data_frame = get_cash_frame(ldt_timestamps, capital, symbols, trade_data_frame, close_data)

    # print cash_data_frame['Cash']

    own_data_frame = pandas.DataFrame(index=ldt_timestamps, columns=symbols)
    for sym in symbols:
        own_data_frame[sym][ldt_timestamps[0]] = 0
    for sym in symbols:
        for i in range(1, len(ldt_timestamps)):
            if trade_data_frame[sym][ldt_timestamps[i]] != 0:
                own_data_frame[sym][ldt_timestamps[i]] = trade_data_frame[sym][ldt_timestamps[i]]
            else:
                own_data_frame[sym][ldt_timestamps[i]] = own_data_frame[sym][ldt_timestamps[i - 1]]

    value_data_frame = own_data_frame.mul(close_data[0], axis=0)

    portfolio_value = pandas.DataFrame(index=ldt_timestamps, columns=['Value'])

    for i in range(0, len(ldt_timestamps)):
        temp_sum = 0
        for sym in symbols:
            temp_sum += value_data_frame[sym][ldt_timestamps[i]]
        temp_sum += cash_data_frame['Cash'][ldt_timestamps[i]]
        portfolio_value['Value'][ldt_timestamps[i]] = temp_sum

    writer = csv.writer(open(output_file, 'wb'), delimiter=',')
    for i in range(0, len(ldt_timestamps)):
        row_to_enter = [ldt_timestamps[i].year, ldt_timestamps[i].month, ldt_timestamps[i].day,
                        portfolio_value['Value'][ldt_timestamps[i]]]
        writer.writerow(row_to_enter)


if __name__ == '__main__':
    main(sys.argv)
