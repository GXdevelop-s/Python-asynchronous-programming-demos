# -*- coding:utf-8 -*-
"""
作者: gaoxu
日期: 2022年01月21日
"""
import asyncio

# 1事件循坏伪代码（ 理解为一个死循环，去检测并执行某些代码）
import requests

'''
任务列表=[任务1,任务2,任务3,...]
while true:
    可执行的任务列表,已完成的任务列表=去任务列表中检查所有的任务，将'可执行'和'已完成'的任务返回
    for 就绪任务 in 可执行的任务列表：
        执行已就绪的任务
    for 已完成的任务 in 已完成的任务列表：
        在任务列表中移除已完成的任务
    如果 任务列表中的任务都已完成，则中止循环

'''
# 去生成或获取一个事件循环
loop = asyncio.get_event_loop()
# 将任务放到任务列表
loop.run_until_complete(任务)



# 2快速上手
'''
协程函数，定义的时候async def 函数名字
协程对象 执行协程函数（）得到的协程对象
'''
async def func():
    pass


# 注意执行协程函数创建协程对象，函数内部代码不会执行
result = func()
loop = asyncio.get_event_loop()
# 如果想要运行协程函数内部代码，必须要将协程对象交给事件循环来处理
loop.run_until_complete(result)  # loop.run_until_complete(func()) 两种写法等价

# python3.7之后，37-39行代码可以被简写为
asyncio.run(result)



# 3await示例
'''
await + 可等待的对象（协程对象、Future对象、Task对象->IO等待）
await就是等待对象的值得到结果之后再继续向下走
'''
async def others():
    print('start')
    await asyncio.sleep(2)
    print('end')
    return '返回值'
async  def f():
    print('执行协程函数内部代码')
    # 遇到IO操作挂起当前协程（任务），等IO操作完成之后再继续向下执行，当协程挂起时，事件循环可以去执行其他协程（任务）
    response1=await others()
    print('IO请求结束，结果为：', response1)
    response2=await others()
    print('IO请求结束，结果为：',response2)
asyncio.run(f())



# 4Task对象
'''
Tasks are used to schedule coroutines concurrently
在事件循环中添加多个任务的
Tasks用于并发调度协程，通过asyncio.create_task(协程对象)的方式创建Task对象，这样可以让协程加入循环中等待被调度执行
除了使用asyncio.create_task()函数以外，还可以用低层级的loop.create_task()或ensure_future()函数
不建议手动实例化Task对象
注意：asyncio.create_task()函数在python3.7中被加入，在之间可以改用低级的asyncio.ensure_future函数
总结：task对象在事件循环中并发的创建多个任务，让事件循环遇到io可以自由切换
'''
async def func():
    print('start')
    await asyncio.sleep(2)
    print('end')
    return '返回值'


async def main():
    print('main开始')
    task_list = [
        # 这段代码会将func这个任务（t1）立即加到事件循环中去
        asyncio.create_task(func(), name='t1'),
        asyncio.create_task(func(), name='t2')
    ]
    print('main结束')
    # done和pending是两个集合，done中是所有task的返回值，pending中是未完成的返回值
    done, pending = await asyncio.wait(task_list, timeout=None)
    print('done')
asyncio.run(main())


# 5 asyncio+不支持异步的模块（两种future）
# 案例及解释（线程和协程的配合）
async def download(url):
    # 发送网络请求，遇到io请求，自动切换到其他任务
    print('开始下载')
    loop = asyncio.get_event_loop()
    # requests模块不支持异步操作，所以就使用线程池来配合实现了
    # run_in_executor函数内部调用了futures.wrap_future（）使得concurrent中的future被封装成了async中的future
    future = loop.run_in_executor(None,requests.get,url)
    response = await future
    print('下载完成')
url_list = [
    'url1',
    'url2',
    'url3'
]
tasks = [download(url) for url in url_list]
loop = asyncio.get_event_loop()
loop.run_until_complete(asyncio.wait(tasks))


# 6 异步迭代器
'''
实现了__aiter__()和__anext__()方法的对象。__anext__必须返回一个awaitable对象
async for 会处理异步迭代器的__anext__()方法所返回的可等待对象，直到其引发一个StopAsyncIteration异常
由PEP292引入
'''
# 异步可迭代对象
'''
可在async语句中被使用的对象。必须通过它的__aiter__()方法返回一个asynchronous iterator
'''
class Reader():
    # 自定义异步迭代器
    def __init__(self):
        self.count = 0
    async def readline(self):
        await asyncio.sleep(1)
        self.count += 1
        if self.count == 100:
            return None
        return self.count
    def __aiter__(self):
        return self
    async def __anext__(self):
        val=await self.readline()
        if val is None:
            raise StopAsyncIteration
        return val
async def func_r():
    obj = Reader()
    # async for 必须写在协程函数内
    async for item in obj:
        print(item)
asyncio.run(func_r())

# 7 异步上下文管理器
'''
此种对象通过定义__aenter__()和__aexit__()方法来对async with语句中的环境进行控制
由PEP 492引入
'''
class AsyncContextManager:
    def __init__(self):
        self.conn = 'conn'
    async def do_sth(self):
        # 异步操作数据库
        return 666
    # 一旦进入上下文管理，就会进入这个函数
    async def __aenter__(self):
        # 异步链接数据库
        self.conn = await asyncio.sleep(1)
        return self # 这里返回什么，下面的f就是什么
    async def __aexit__(self):
        # 异步关闭数据库链接
        await asyncio.sleep(1)

# async with 也要放在协程函数里面
async def fun_m():
    # 进入上下文管理
    async with AsyncContextManager() as f:
        result_m = await f.do_sth()
        print(result_m)
asyncio.run(fun_m())



