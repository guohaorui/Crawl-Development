# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
import pymysql


class ScrapyQuotePipeline:
    fp = None

    def open_spider(self, spider):
        print('开始爬虫.....')
        self.fp = open('./data_pipeline.txt', 'w', encoding='utf-8')

    def process_item(self, item, spider):
        author = item['author']
        content = item['content']
        tags = item['tags']

        self.fp.write(f'{author}:{content}:{tags}\n')
        return item

    def close_spider(self, spider):
        print('结束爬虫')
        self.fp.close()


class MysqlPipeline:
    conn = None
    cursor = None

    def open_spider(self, spider):
        self.conn = pymysql.Connect(host='180.76.106.23', port=3306, user='root', password='123456', db='scrapy_quote')
        # self.cursor = self.conn.cursor()

    def process_item(self, spider):
        self.cursor = self.conn.cursor()
        pass
