# -*- coding:utf-8 -*-
"""
作者: gaoxu
日期: 2022年01月20日
"""
import asyncio

'''
弄清楚了asyncio.coroutine和yield from之后，在Python3.5中引入的async和await就不难理解了：可以将他们理解成asyncio.coroutine/yield from的完美替身
本质上干的事情是一样的，引入了关键字，就更为简洁
'''


async def func1():
    print(1)
    # python3.5 不支持yield from(实际上是解析了)在async函数内
    await asyncio.sleep(2)  # 遇到io耗时操作，自动切换到tasks中的其他任务

    print(2)


async def func2():
    print(3)
    await asyncio.sleep(2)  # 遇到耗时操作，自动切换到tasks中的其他任务
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
