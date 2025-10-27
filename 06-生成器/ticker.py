# ticker.py

from follow import follow
import csv
from tableformat import TableFormatter as tableformatter
import report

def convert_types(rows,types):
    for row in rows:
        yield [func(val) for func, val in zip(types, row)]

def make_dicts(rows, headers):
    for row in rows:
        yield dict(zip(headers, row))

def select_columns(rows, indices):
    for row in rows:
        yield [row[index] for index in indices]

def parse_stock_data(lines):
    rows = csv.reader(lines)
    rows = select_columns(rows, [0,1,4])
    rows = convert_types(rows, [str,float,float])
    rows = make_dicts(rows, ['name','price','change'])
    return rows

def filter_symbols(rows, names):
    for row in rows:
        if row['name'] in names:
            yield row
def ticker(portfile, logfile, fmt):
    portfolio = report.read_portfolio(portfile)
    rows = parse_stock_data(follow('stocklog.csv'))
    rows = filter_symbols(rows, portfolio)
    formatter = tableformatter.create_formatter(fmt)
    formatter.headings(('名称', '价格', '变化'))
    for row in rows:
        formatter.row([ row['name'], f"{row['price']:0.2f}", f"{row['change']:0.2f}"] )


if __name__ == '__main__':
    ticker('../Data/portfolio.csv', 'stocklog.csv', 'txt')
    # import report
    # portfolio = report.read_portfolio('../Data/portfolio.csv')
    # print( portfolio)
    # rows = parse_stock_data(follow('stocklog.csv'))
    # rows = filter_symbols(rows, portfolio)
    # for row in rows:
    #     print(row)