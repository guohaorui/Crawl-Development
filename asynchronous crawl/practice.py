# -*- coding:utf-8 -*-
"""
@Author      :   Haorui Guo
@File        :   practice.py
@Contact     :   12032793@mail.sustech.edu.cn
@Modify Time :   2022/12/5
"""
# 崔庆才作业
# 异步爬取https://spa5.scrape.center/page/1

import asyncio
import aiohttp
import logging

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s: %(message)s')

import json

from motor.motor_asyncio import AsyncIOMotorClient

MONGO_USER = 'admin'
MONGO_PASSWORD = '123456'
MONGO_CONNECTION_STRING = 'mongodb://{}:{}@180.76.106.23:27017'.format(MONGO_USER, MONGO_PASSWORD)
MONGO_DB_NAME = 'crawl_test'
MONGO_COLLECTION_NAME = 'spa5_books'
client = AsyncIOMotorClient(MONGO_CONNECTION_STRING)
db = client[MONGO_DB_NAME]
collection = db[MONGO_COLLECTION_NAME]

INDEX_URL = 'https://spa5.scrape.center/api/book/?limit=18&offset={offset}'
DETAIL_URL = 'https://spa5.scrape.center/api/book/{id}'

PAGE_SIZE = 18
PAGE_NUMBER = 10
CONCURRENCY = 5

semaphore = asyncio.Semaphore(CONCURRENCY)
session = None


async def save_data(data):
    logging.info('Saving data %s', data)
    if data:
        result = await collection.update_one({
            'id': data.get('id')
        }, {
            '$set': data
        }, upsert=True)
        return result


async def scrape_api(url):
    async with semaphore:
        try:
            logging.info('Scraping %s', url)
            async with session.get(url) as response:
                return await response.json()
        except aiohttp.ClientError:
            logging.error('Error occurred while scraping url %s', url, exc_info=True)


async def scrape_index(page):
    url = INDEX_URL.format(offset=PAGE_SIZE * (page - 1))
    return await scrape_api(url)


async def scrape_detail(id):
    url = DETAIL_URL.format(id=id)
    data = await scrape_api(url)
    await save_data(data)


async def main():
    global session
    session = aiohttp.ClientSession()
    # 1. 爬取列表页
    scrape_index_tasks = [asyncio.ensure_future(scrape_index(i)) for i in range(1, PAGE_NUMBER + 1)]
    results = await asyncio.gather(*scrape_index_tasks)
    logging.info('Results %s', json.dumps(results, ensure_ascii=False, indent=2))

    # 2. 爬取详情页
    ids = []
    for index_data in results:
        if not index_data: continue
        for item in index_data.get('results'):
            ids.append(item.get('id'))
    scrape_detail_tasks = [asyncio.ensure_future(scrape_detail(id)) for id in ids]
    # wait和gather效果一样，但是返回效果略有差异
    await asyncio.wait(scrape_detail_tasks)
    # 记住需要关闭session
    await session.close()


if __name__ == '__main__':
    asyncio.run(main())
