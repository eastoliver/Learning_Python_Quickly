# follow.py
import os
import time

def follow(filename):
    '''
    生成器，用于在文件末尾写入一系列行。
    '''
    f = open(filename, 'r')
    f.seek(0, os.SEEK_END)
    while True:
        line = f.readline()
        if line == '':
            time.sleep(0.1)  # 0.1秒后继续
            continue
        yield line

if __name__ == '__main__':
    import report

    portfolio = report.read_portfolio('../Data/portfolio.csv')

    for line in follow('stocklog.csv'):
        row = line.split(',')
        name = row[0].strip('"')
        price = float(row[1])
        change = float(row[4])
        if name in portfolio:
            print(f'{name:>8s} {price:>8.2f} {change:>8.2f}')
