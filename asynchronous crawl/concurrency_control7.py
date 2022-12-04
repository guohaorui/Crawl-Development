# -*- coding:utf-8 -*-
"""
@Author      :   Haorui Guo
@File        :   concurrency_control7.py
@Contact     :   12032793@mail.sustech.edu.cn
@Modify Time :   2022/12/4
"""
# 并发大小要好好控制
from utils import *

CONCURRENCY = 5
url = 'https://www.baidu.com'

semaphore = asyncio.Semaphore(CONCURRENCY)
session = None


async def scrape_api():
    async with semaphore:
        print('Scraping', url)
        async with session.get(url) as response:
            await asyncio.sleep(1)
            return await response.text()


async def main():
    global session
    session = aiohttp.ClientSession()
    scrape_tasks = [asyncio.ensure_future(scrape_api()) for _ in range(10000)]
    await asyncio.gather(*scrape_tasks)

if __name__ == '__main__':
    asyncio.run(main())