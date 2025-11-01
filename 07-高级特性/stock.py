from typedproperty import String, Integer, Float


class Stock:
    """
    股票类
    """
    name = String('name')
    shares = Integer('shares')
    price = Float('price')


    def __repr__(self):
        return f'Stock({self.name!r},{self.shares!r},{self.price!r})'

    def __init__(self, name, shares, price):
        self.name = name
        self.shares = shares
        self.price = price

    @property  # 属性方法
    def cost(self):
        """
        计算股票价值
        """
        return self.shares * self.price

    def sell(self, nshares):
        """
        出售股票
        """
        self.shares -= nshares


if __name__ == '__main__':
    s = Stock('GOOG', 100, 490.1)
    print(s)