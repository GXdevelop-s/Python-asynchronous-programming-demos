# -*- coding:utf-8 -*-
"""
作者: gaoxu
日期: 2022年01月20日
"""
import asyncio

'''
yield就是将range这个可迭代对象直接返回了。
而yield from解析了range对象，将其中每一个item返回了。
yield from iterable本质上等于for item in iterable: yield item的缩写版
yield from后面必须跟iterable对象
yield from在asyncio模块中得以发扬光大。之前都是我们手工切换协程，现在当声明函数为协程后，我们通过事件循环来调度协程。
yield from asyncio.sleep(sleep_secs) 这里不能用time.sleep(1)因为time.sleep()返回的是None，它不是iterable
'''


@asyncio.coroutine
def func1():
    print(1)
    # python3.5 不支持yield from(实际上是解析了)在async函数内
    yield from asyncio.sleep(2)# 遇到io耗时操作，自动切换到tasks中的其他任务

    print(2)


@asyncio.coroutine
def func2():
    print(3)
    yield from asyncio.sleep(2)  # 遇到耗时操作，自动切换到tasks中的其他任务
    print(4)


# 把任务封装起来
tasks = [
    # 把async函数封装成future对象
    asyncio.ensure_future(func1()),
    asyncio.ensure_future(func2())
]

# 将任务加载到loop中
loop = asyncio.get_event_loop()
loop.run_until_complete(asyncio.wait(tasks))
