# -*- coding:utf-8 -*-
"""
@Author      :   Haorui Guo
@File        :   usage.py
@Contact     :   12032793@mail.sustech.edu.cn
@Modify Time :   2022/12/5
"""

import requests

proxypool_url = 'http://180.76.106.23:5555/random'
# target_url = 'http://httpbin.org/get'
target_url = 'https://antispider5.scrape.center/'


def get_random_proxy():
    """
    get random proxy from proxypool
    :return: proxy
    """
    return requests.get(proxypool_url).text.strip()


def crawl(url, proxy):
    """
    use proxy to crawl page
    :param url: page url
    :param proxy: proxy, such as 8.8.8.8:8888
    :return: html
    """
    proxies = {'http': 'http://' + proxy}
    return requests.get(url, proxies=proxies).text


def main():
    """
    main method, entry point
    :return: none
    """
    proxy = get_random_proxy()
    print('get random proxy', proxy)
    html = crawl(target_url, proxy)
    print(html)


if __name__ == '__main__':
    main()
