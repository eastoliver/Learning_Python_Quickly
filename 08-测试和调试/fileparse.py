# fileparse.py
import csv
import logging
log = logging.getLogger(__name__)

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
                    log.warning(f"第{rowno}行: 无法转换 {row}")
                    log.debug(f"第{rowno}行: 原因 {e}")
                continue

        # 创建字典或元组
        if headers:
            record = dict(zip(headers, row))
        else:
            record = tuple(row)
        records.append(record)

    return records

def split(line, types=None, names=None, delimiter=None):
    """分割字符串并应用类型转换"""
    items = line.split(delimiter if delimiter else None)

    if types:
        items = [func(item) for func, item in zip(types, items)]

    if names:
        return dict(zip(names, items))

    return items

def parse(f, types=None, names=None, delimiter=None):
    records = []
    for line in f:
        line = line.strip() # 去除行首尾空白
        if not line:
            continue
        try:
            records.append(split(line, types, names, delimiter))
        except ValueError as e:
            logging.warning(f"行 {line} 无法转换: {e}")
    return records

def main():
    # 配置日志系统
    logging.basicConfig(
        filename='app.log', # 日志文件
        level=logging.WARNING,  # 记录级别
        format='%(asctime)s %(name)-12s %(levelname)-8s %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S',
        encoding='utf-8'
    )
    # 示例数据
    data = [
        "1,2,3",
        "a,b,c",    # 这行会触发警告
        "4,5,6"
    ]

    # 调用解析函数
    result = parse(data,types=[int, int, int], names=['x', 'y', 'z'],delimiter=',')
    print("解析结果：",result)

if __name__ == '__main__':
    # 使用示例
    # with open('Data/portfolio.csv', 'rt', encoding='utf-8') as f:
    #     lines = f.readlines()
    #     portfolio = parse_csv(lines, select=['name', 'shares', 'price'], types=[str, int, float])
    #     print(portfolio)

    # portfolio = parse_csv('Data/missing.csv', types=[str, int, float])
    # print(portfolio)

    # main()
    import  report
    logging.getLogger(__name__).level = logging.CRITICAL
    a = report.read_portfolio('../Data/missing.csv')