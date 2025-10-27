# report.py
from fileparse import parse_csv


def read_portfolio(filename):
    '''
    将股票投资组合文件读取为包含名称、股份数量和价格键的字典列表。
    '''
    # 使用parse_csv进行类型转换
    with open(filename) as lines:
        portfolio = parse_csv(lines,select=['name','shares','price'], types=[str, int, float])
    return portfolio


def read_prices(filename):
    '''
    将CSV价格数据文件读取为将名称映射到价格的字典。
    '''
    # 使用parse_csv读取无标题文件获取元组，然后转换为字典
    with open(filename) as lines:
        price_tuples = parse_csv(lines, has_headers=False, types=[str, float], silence_errors=True)
        prices = {name: price for name, price in price_tuples}
        return prices


def make_report_data(portfolio, prices):
    '''
    给定投资组合列表和价格字典，生成(名称, 股份数量, 价格, 变化)元组列表。
    '''
    rows = []
    for stock in portfolio:
        current_price = prices[stock['name']]
        change = current_price - stock['price']
        summary = (stock['name'], stock['shares'], current_price, change)
        rows.append(summary)
    return rows


def print_report(portfolio_file, prices_file):
    '''
    打印投资组合表现报告。
    '''
    portfolio = read_portfolio(portfolio_file)
    prices = read_prices(prices_file)
    report = make_report_data(portfolio, prices)
    
    headers = ('名称', '股份数量', '价格', '变化')
    print('%10s %10s %10s %10s' % headers)
    print(('-' * 10 + ' ') * len(headers))
    for name, shares, price, change in report:
        print(f'{name:>10s} {shares:>10d} {price:>10.2f} {change:>10.2f}')


def portfolio_report(portfolio_filename, prices_filename):
    '''
    生成并打印投资组合报告。
    '''
    print_report(portfolio_filename, prices_filename)

def main(args):
    if len(args) != 3:
        raise SystemExit('Usage: %s portfoliofile pricesfile' % args[0])
    portfolio_report(args[1], args[2])

if __name__ == '__main__':
    import sys
    main(sys.argv)
    # portfolio_report('Data/portfolio.csv', 'Data/prices.csv')