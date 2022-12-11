# -*- coding:utf-8 -*-
"""
@Author      :   Haorui Guo
@File        :   spider.py
@Contact     :   12032793@mail.sustech.edu.cn
@Modify Time :   2022/12/9
"""
from requests import Session
from db import RedisQueue
from practice import MovieRequest
from fake_headers import Headers
from loguru import logger
import requests
from urllib.parse import urljoin
import re
from pyquery import PyQuery as pq

PROXY_POOL_URL = 'http://180.76.106.23:5555/random'
BASE_URL = 'https://antispider5.scrape.center/'

headers = Headers(browser='Chrome')
HEADERS = headers.generate()

VALID_STATUSES = [200]
MAX_FAIL_TIME = 10


class Spider():
    session = Session()
    queue = RedisQueue()

    def start(self):
        self.session.headers.update(HEADERS)
        start_url = BASE_URL
        request = MovieRequest(url=start_url, callback=self.parse_index)
        self.queue.add(request)

    def schedule(self):
        while not self.queue.empty():
            request: MovieRequest = self.queue.pop()
            callback = request.callback
            logger.debug(f'Executing request {request.url}')
            response = self.request(request)
            if not response or response.status_code not in VALID_STATUSES:
                self.error(request)
                continue

            results = list(callback(response))
            if not results:
                self.error(request)
                continue
            for result in results:
                if isinstance(result, MovieRequest):
                    logger.debug(f'Generated new index request {result}')
                    self.queue.add(result)
                if isinstance(result, dict):
                    logger.debug(f'Scraped new detail data {result}')

    def error(self, req: MovieRequest):
        req.fail_time += 1
        logger.debug(f'Request of url {req.url} failed {req.fail_time} times')
        if req.fail_time < MAX_FAIL_TIME:
            self.queue.add(req)

    def parse_index(self, response):
        doc = pq(response.text)

        # request for detail
        items = doc('.item .name').items()
        for item in items:
            detail_url = urljoin(BASE_URL, item.attr('href'))
            request = MovieRequest(url=detail_url, callback=self.parse_detail)
            yield request

        # request for next page
        next_href = doc('.next').attr('href')
        if next_href:
            next_url = urljoin(BASE_URL, next_href)
            request = MovieRequest(
                url=next_url, callback=self.parse_index)
            yield request

    def parse_detail(self, response):
        doc = pq(response.text)
        cover = doc('img.cover').attr('src')
        name = doc('a > h2').text()
        categories = [item.text()
                      for item in doc('.categories button span').items()]
        published_at = doc('.info:contains(上映)').text()
        published_at = re.search('(\d{4}-\d{2}-\d{2})', published_at).group(1) \
            if published_at and re.search('\d{4}-\d{2}-\d{2}', published_at) else None
        drama = doc('.drama p').text()
        score = doc('p.score').text()
        score = float(score) if score else None
        yield {
            'cover': cover,
            'name': name,
            'categories': categories,
            'published_at': published_at,
            'drama': drama,
            'score': score
        }

    @logger.catch
    def request(self, req: MovieRequest):
        proxy = self.get_proxy()
        logger.debug(f'Get proxy {proxy} in request()')
        proxies = {
            'http': 'http://' + proxy
            # 'https': 'https://' + proxy
        } if proxy else None
        return self.session.send(req.prepare(), timeout=req.timeout, proxies=proxies)

    @logger.catch
    def get_proxy(self):
        response = requests.get(PROXY_POOL_URL)
        if response.status_code == 200:
            logger.debug(f'Get proxy {response.text}')
            return response.text

    def run(self):
        self.start()
        self.schedule()


if __name__ == '__main__':
    spider = Spider()
    spider.run()
