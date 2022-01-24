# -*- coding:utf-8 -*-
"""
作者: gaoxu
日期: 2022年01月20日
"""


def func1():
    yield 1
    yield from func2()
    yield 2


def func2():
    yield 3
    yield 4


f1 = func1()
for item in f1:
    print(item)
