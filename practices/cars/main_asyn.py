# -*- coding:utf-8 -*-
"""
@Author      :   Haorui Guo
@File        :   main_asyn.py
@Contact     :   12032793@mail.sustech.edu.cn
@Modify Time :   2022/12/5
"""

import asyncio
import datetime
import os

import aiohttp
import logging
import json
import pandas as pd
import time

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s: %(message)s')

CONCURRENCY = 5
N = 5

semaphore = asyncio.Semaphore(CONCURRENCY)
session = None

END_DATE = datetime.date(2022, 12, 4)
START_DATE = datetime.date(2022, 10, 1)
N = (END_DATE - START_DATE).days + 1

URL = 'https://index.dongchedi.com/dzx_index/rank/list'
COOKIES = {
    'MONITOR_WEB_ID': '57a7c5f1-5de0-412f-be44-0a9eed9d0dae',
    'tea_session': '23b34ff3-7a38-4bfd-825f-80ef81847872%2C1670125525733',
}

HEADERS = {
    'authority': 'index.dongchedi.com',
    'accept': 'application/json, text/plain, */*',
    'accept-language': 'zh-CN,zh;q=0.9',
    'referer': 'https://index.dongchedi.com/rank?rank_type=%E5%93%81%E7%89%8C&date=2022-11-13&price=%E5%85%A8%E9%83%A8%E4%BB%B7%E6%A0%BC',
    'sec-ch-ua': '"Google Chrome";v="107", "Chromium";v="107", "Not=A?Brand";v="24"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Windows"',
    'sec-fetch-dest': 'empty',
    'sec-fetch-mode': 'cors',
    'sec-fetch-site': 'same-origin',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/107.0.0.0 Safari/537.36',
}


async def scrape_api(params):
    async with semaphore:
        try:
            logging.info('Scraping %s with params %s', URL, params)
            async with session.get(URL, params=params, cookies=COOKIES, headers=HEADERS) as response:
                return await response.json()
        except aiohttp.ClientError:
            logging.error('Error occurred while scraping url %s with params %s', URL, params, exc_info=True)


async def scrape_data(rank_type, date):
    store_file_path = './data/{}_{}.xlsx'.format(rank_type, date.replace('-', '_'))
    if os.path.exists(store_file_path):
        return

    params = {
        'rank_type': rank_type,
        'date': date,
        'sub_rank_type': '全部新能源',
        'price': '全部价格',
        'province': '全国',
    }

    response = await scrape_api(params)
    datas = response['data']['form_data']['data']
    ITEMS = []
    if not datas:
        logging.info('No data requests with params %s', params)
        return

    for data in datas:
        item = {
            'id': data['id'],
            '品牌名称': data['name'],
            '价格': data['price'],
            '懂车指数': data['index_value'],
            '日环比': data['index_hb'],
            '汽车图标': data['url'],
            '榜单类型': rank_type,
            '日期': date,
        }
        ITEMS.append(item)
    df = pd.DataFrame(ITEMS)
    df.to_excel(store_file_path)
    logging.info('Store {} elements to {}'.format(len(datas), store_file_path))


async def main():
    global session
    session = aiohttp.ClientSession()

    scrape_index_tasks = []
    rank_type = '新能源榜单'
    for day in range(N):
        date = (END_DATE - datetime.timedelta(days=day)).strftime('%Y-%m-%d')
        scrape_index_tasks.append(asyncio.ensure_future(scrape_data(rank_type, date)))
    await asyncio.gather(*scrape_index_tasks)
    logging.info('Tasks finished')

    await session.close()


if __name__ == '__main__':
    asyncio.run(main())
