# -*- coding:utf-8 -*-
"""
作者: gaoxu
日期: 2022年02月05日
"""
import time

import aiohttp
import asyncio


async def download(url):
    # 与request不同的是，aiohttp需要借助ClientSession来发送请求
    async with aiohttp.ClientSession() as session:
        # get()、post()
        # hearders params proxy
        head = {
            'User-Agent': 'Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/97.0.4692.71 Mobile Safari/537.36'
        }
        async with await session.get(url,headers=head) as response:
            # text()返回字符串形式的响应数据
            # read()返回的二进制形式的响应数据
            # json()返回的就是json对象
            # 注意： 获取响应数据操作之前一定要使用await进行手动挂起
            page_text = await response.text()
            #print(page_text)


urls = [
    'https://www.baidu.com/s?tn=baidutop10&wd=%E5%86%B0%E9%9B%AA%E4%B8%BA%E5%AA%92%20%E5%85%B1%E8%B5%B4%E5%86%AC%E5%A5%A5%E4%B9%8B%E7%BA%A6&rsv_idx=2&ie=utf-8&rsv_pq=c3b641e10016a25d&oq=%E5%BC%A0%E8%89%BA%E8%B0%8B%E5%9B%9E%E5%BA%94%E7%94%B5%E5%BD%B1%E6%8E%92%E7%89%87%E9%81%87%E5%86%B7%3A%E9%A1%BE%E4%B8%8D%E4%B8%8A%E4%BA%86&rsv_t=62cbaKXYZF8Nsk0wT%2FXB67uFKyYoNBZQKwMxGYm0lPvwexbIi%2BKhd31gXtyDhehHCg&rqid=c3b641e10016a25d&rsf=c07ff5f00df0efa4cda6cf9183108653_1_15_1&rsv_dl=0_right_fyb_pchot_20811&sa=0_right_fyb_pchot_20811',
    'https://www.baidu.com/s?tn=baidutop10&wd=%E6%8E%89%E9%98%9F%E7%9A%84%E5%B0%8F%E9%B8%BD%E5%AD%90%E6%98%AF%E8%BF%99%E6%A0%B7%E4%BA%A7%E7%94%9F%E7%9A%84&rsv_idx=2&usm=1&ie=utf-8&rsv_pq=cadac29900048bdf&oq=%E5%86%B0%E9%9B%AA%E4%B8%BA%E5%AA%92%20%E5%85%B1%E8%B5%B4%E5%86%AC%E5%A5%A5%E4%B9%8B%E7%BA%A6&rsv_t=e27bSAoayz8rQY3VL5mJlZ0DAVKZkOUyJJ6tMFX8GDANmTFHElKrHu1YLOsB6xDX7w&rqid=cadac29900048bdf&rsf=c07ff5f00df0efa4cda6cf9183108653_1_15_2&rsv_dl=0_right_fyb_pchot_20811&sa=0_right_fyb_pchot_20811',
    'https://www.baidu.com/s?tn=baidutop10&wd=%E5%86%AC%E5%A5%A5%E4%BC%9A%E5%BC%80%E5%B9%95%E5%BC%8F10%E4%B8%AA%E9%9A%BE%E5%BF%98%E7%9E%AC%E9%97%B4&rsv_idx=2&usm=1&ie=utf-8&rsv_pq=c4de733600159942&oq=%E6%8E%89%E9%98%9F%E7%9A%84%E5%B0%8F%E9%B8%BD%E5%AD%90%E6%98%AF%E8%BF%99%E6%A0%B7%E4%BA%A7%E7%94%9F%E7%9A%84&rsv_t=38bdKgzCIjD5edQ3WpkAmj91%2FppM85ZT2E%2F9X65MWcn%2FKKcmI7KznK1Bti2xUHK3zw&rqid=c4de733600159942&rsf=c07ff5f00df0efa4cda6cf9183108653_1_15_3&rsv_dl=0_right_fyb_pchot_20811&sa=0_right_fyb_pchot_20811'
]


async def main():
    task_list = [asyncio.create_task(download(url)) for url in urls]
    done, pending = await asyncio.wait(task_list, timeout=10)
    print(done)


t1 = time.time()
# asyncio.run(main())改用loop
# aiohttp 内部使用了 _ProactorBasePipeTransport ，程序退出释放内存时自动调用其 __del__ 方法导致二次关闭事件循环。
# 一般的协程程序是不会使用_ProactorBasePipeTransport 的，所以asyncio.run() 还是可以正常运行。而且这种情况仅在Windows上发生
loop = asyncio.get_event_loop()
loop.run_until_complete(main())
print('整体时间：', time.time() - t1)
