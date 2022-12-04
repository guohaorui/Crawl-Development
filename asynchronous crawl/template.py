# -*- coding:utf-8 -*-
"""
@Author      :   Haorui Guo
@File        :   template.py
@Contact     :   12032793@mail.sustech.edu.cn
@Modify Time :   2022/12/5
"""
import asyncio
import aiohttp
import logging
import json

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s: %(message)s')

CONCURRENCY = 5
N = 5

semaphore = asyncio.Semaphore(CONCURRENCY)
session = None


async def scrape_api(url):
    async with semaphore:
        try:
            logging.info('Scraping %s', url)
            async with session.get(url) as response:
                return await response.json()
        except aiohttp.ClientError:
            logging.error('Error occurred while scraping url %s', url, exc_info=True)


async def scrape_xxx():
    pass


async def main():
    global session
    session = aiohttp.ClientSession()

    scrape_index_tasks = [asyncio.ensure_future(scrape_xxx()) for i in range(1, N)]
    results = await asyncio.gather(*scrape_index_tasks)
    logging.info('Results %s', json.dumps(results, ensure_ascii=False, indent=2))

    await session.close()


if __name__ == '__main__':
    asyncio.run(main())
