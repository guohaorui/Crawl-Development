# -*- coding:utf-8 -*-
"""
@Author      :   Haorui Guo
@File        :   routine1.py
@Contact     :   12032793@mail.sustech.edu.cn
@Modify Time :   2022/12/4
"""
# 当爬取https://www.httpbin.org/delay/5时，需要等待5秒才能获取结果，如果遍历100次这个网站，单线程就需要500s，协程就不一样了
import logging
import requests
import time

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s: %(message)s')
TOTAL_NUMBER = 5
URL = 'https://www.httpbin.org/delay/5'

start_time = time.time()
for _ in range(1, TOTAL_NUMBER + 1):
    logging.info('scraping %s', URL)
    response = requests.get(URL)
end_time = time.time()
logging.info('total time %s seconds', end_time - start_time)
