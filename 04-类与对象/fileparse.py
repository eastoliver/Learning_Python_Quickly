# fileparse.py
import csv

def parse_csv(lines, select=None, types=None, has_headers=True, delimiter=',', silence_errors=False):
    '''
    将CSV文件解析为记录列表，并支持类型转换。
    '''
    if select and not has_headers:
        raise RuntimeError('select参数需要列标题')


    rows = csv.reader(lines, delimiter=delimiter)

    # 读取文件标题（如果有）
    headers = next(rows) if has_headers else []

    # 如果选择了特定列，则创建索引进行过滤并设置输出列
    if select:
        indices = [ headers.index(colname) for colname in select ]
        headers = select

    records = []
    for rowno, row in enumerate(rows, 1):
        if not row:     # 跳过空行
            continue

        # 如果选择了特定列索引，则提取这些列
        if select:
            row = [ row[index] for index in indices]

        # 对行应用类型转换
        if types:
            try:
                row = [func(val) for func, val in zip(types, row)]
            except ValueError as e:
                if not silence_errors:
                    print(f"第{rowno}行: 无法转换 {row}")
                    print(f"第{rowno}行: 原因 {e}")
                continue

        # 创建字典或元组
        if headers:
            record = dict(zip(headers, row))
        else:
            record = tuple(row)
        records.append(record)

    return records


if __name__ == '__main__':
    # 使用示例
    with open('Data/portfolio.csv', 'rt', encoding='utf-8') as f:
        lines = f.readlines()
        portfolio = parse_csv(lines, select=['name', 'shares', 'price'], types=[str, int, float])
        print(portfolio)
    # portfolio = parse_csv('Data/missing.csv', types=[str, int, float])
    # print(portfolio)