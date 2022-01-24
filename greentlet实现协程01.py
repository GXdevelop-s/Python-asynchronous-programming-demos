# -*- coding:utf-8 -*-
"""
作者: gaoxu
日期: 2022年01月20日
"""
from greenlet import greenlet


def func1():
    print(1)
    gr2.switch()
    print(2)
    gr2.switch()


def func2():
    print(3)
    gr1.switch()
    print(4)


gr1 = greenlet(func1)
gr2 = greenlet(func2)
gr1.switch()