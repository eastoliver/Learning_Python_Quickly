class Stock :
    """
    股票类
    """
    __slots__ = ('name', '_shares', 'price')
    
    def __repr__(self):
        return f'Stock({self.name},{self.shares},{self.price})'

    def __init__(self, name, shares, price):
        self.name = name
        self.shares = shares
        self.price = price

    @property
    def shares(self):
        return self._shares

    @shares.setter
    def shares(self, value):
        if not isinstance(value, int):
            raise TypeError('shares必须为整数')
        self._shares = value

    @ property # 属性方法
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