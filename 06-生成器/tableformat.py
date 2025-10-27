class TableFormatter:
    """
    表格格式抽象类
    """
    @classmethod
    def create_formatter(cls, fmt):
        if fmt == 'txt':
            formatter = TextTableFormatter()
        elif fmt == 'csv':
            formatter = CSVTableFormatter()
        elif fmt == 'html':
            formatter = HTMLTableFormatter()
        else:
            raise FormatError(f'{fmt}')
        return formatter


    def headings(self, headers):
        '''
        Emit the table headings.
        '''
        raise NotImplementedError()

    def row(self, rowdata):
        '''
        Emit a single row of table data.
        '''
        raise NotImplementedError()

class TextTableFormatter(TableFormatter):
    """
    输出为纯文本的表格格式
    """
    def headings(self, headers):
        for h in headers:
            print(f'{h:>8s}', end=' ')
        print()
        print(('-'*10 + ' ')*len(headers))

    def row(self, rowdata):
        for i, d in enumerate(rowdata):
            # 根据用户偏好，价格列的$符号应紧贴数字
            if i == 2 and d.startswith('$'):
                # 对于价格列，格式化为$符号紧贴数字，总宽度为10
                print(f'${d[1:]:>9s}', end=' ')
            else:
                print(f'{d:>10s}', end=' ')
        print()

class CSVTableFormatter(TableFormatter):
    """
    输出为CSV格式的表格
    """
    def headings(self, headers):
        print(','.join(headers))
    def row(self, rowdata):
        print(','.join(rowdata))

class HTMLTableFormatter(TableFormatter):
    """
    输出为HTML格式的表格
    """
    def headings(self, headers):
        print('<tr>', end='')
        for h in headers:
            print(f'<th>{h}</th>', end='')
        print('</tr>')
    def row(self, rowdata):
        print('<tr>', end='')
        for d in rowdata:
            print(f'<td>{d}</td>', end='')
        print('</tr>')

class FormatError(Exception):
    def __init__(self, fmt):
        super().__init__()
        print(f'FormatError: Unknown table format {fmt}')

def print_table(objects, columns, formatter):
    '''
    Make a nicely formatted table from a list of objects and attribute names.
    '''
    formatter.headings(columns)
    for obj in objects:
        rowdata = [ str(getattr(obj, name)) for name in columns ]
        formatter.row(rowdata)

if __name__ == '__main__':
    from tableformat import TableFormatter
    formatter = TableFormatter.create_formatter('xls')