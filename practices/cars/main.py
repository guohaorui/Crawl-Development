# -*- coding:utf-8 -*-
"""
@Author      :   Haorui Guo
@File        :   main.py
@Contact     :   12032793@mail.sustech.edu.cn
@Modify Time :   2022/12/4
"""
import os
import time
import requests
import datetime
import pandas as pd

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


def get_data(rank_type, date):
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

    response = requests.get('https://index.dongchedi.com/dzx_index/rank/list', params=params, cookies=COOKIES,
                            headers=HEADERS).json()

    datas = response['data']['form_data']['data']
    ITEMS = []
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
    print('保存{}数据至{}'.format(len(datas), store_file_path))


def main():
    time_1 = datetime.date(2022, 12, 3)  # 指定结束日期
    time_2 = datetime.date(2022, 11, 1)  # 指定起始日期
    n = (time_1 - time_2).days + 1
    for d in range(n):
        yesterday = (time_1 - datetime.timedelta(days=d)).strftime('%Y-%m-%d')
        date = yesterday
        print(f'>> 正在获取 {date} 的数据')
        get_data('新能源榜单', date)
        time.sleep(0.5)


if __name__ == '__main__':
    main()
