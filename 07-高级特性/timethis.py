# timethis.py
import time


def timethis(func):
    """
    记录函数运行时间
    """
    def wrapper(*args, **kwargs):
        start = time.time()
        r = func(*args, **kwargs)
        end = time.time()
        print(f'{func.__module__}.{func.__name__} 运行时间: {end-start:f}s')
    return  wrapper

if __name__ == '__main__':
    @timethis
    def countdown(n):
        while n > 0:
            n -= 1
    countdown(10000000)