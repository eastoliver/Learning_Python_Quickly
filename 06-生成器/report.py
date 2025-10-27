# report.py
import fileparse
from fileparse import parse_csv
from Stock import Stock
from portfolio import Portfolio
from tableformat import TableFormatter as tableformatter
from tableformat import print_table

def read_portfolio(filename):
    '''
    将股票投资组合文件读取为Stock对象列表。
    '''
    # 使用parse_csv读取数据
    with open(filename) as lines:
        portdicts = fileparse.parse_csv(lines, select=['name','shares','price'], types=[str, int, float])

    # 将字典转换为Stock对象
    portfolio = [Stock(d['name'], d['shares'], d['price']) for d in portdicts]
    return Portfolio(portfolio)


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
        current_price = prices[stock.name]
        change = current_price - stock.price
        summary = (stock.name, stock.shares, current_price, change)
        rows.append(summary)
    return rows


def print_report(reportdata, formatter):
    '''
    打印投资组合表现报告。
    '''
    formatter.headings(('名称', '股份数量', '价格', '变化'))
    for name, shares, price, change in reportdata:
        formatter.row([name, str(shares), f'${price:0.2f}', f'{change:0.2f}'])
        # 根据用户偏好，$符号应紧贴数字，空格放在$符号前面
        # print(f'{name:>10s} {shares:>10d} ${price:>9.2f} {change:>10.2f}')


def portfolio_report(portfolio_file, prices_file, fmt='txt'):
    '''
    生成并打印投资组合报告。
    '''
    portfolio = read_portfolio(portfolio_file)
    prices = read_prices(prices_file)
    report = make_report_data(portfolio, prices)
    # 现在可以作为类方法直接调用
    formatter = tableformatter.create_formatter(fmt)
    print_report(report, formatter)

def main(args):
    if len(args) < 3:
        raise SystemExit('Usage: %s portfoliofile pricesfile' % args[0])
    portfolio_report(args[1], args[2], args[3])

if __name__ == '__main__':
    # import sys
    # main(sys.argv)
    import report

    report.portfolio_report('../Data/portfolio.csv', '../Data/prices.csv')