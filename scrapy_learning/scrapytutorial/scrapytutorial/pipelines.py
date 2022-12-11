# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
from scrapy.exceptions import DropItem
import pymongo


class MongoDBPipeline(object):
    def __init__(self, connection_string, databse):
        self.connection_string = connection_string
        self.database = databse

    @classmethod
    def from_crawler(cls, crawler):
        # 获取settings.py中的配置
        return cls(connection_string=crawler.settings.get('MONGODB_CONNECTION_STRING'),
                   databse=crawler.settings.get('MONGODB_DATABASE'))

    def open_spider(self, spider):
        # 当spider启动时调用这个方法
        self.client = pymongo.MongoClient(self.connection_string)
        self.db = self.client[self.database]

    def process_item(self, item, spider):
        name = item.__class__.__name__
        self.db[name].insert_one(dict(item))
        return item

    def close_spider(self, spider):
        # 当spider结束时调用这个方法
        self.client.close()


class TextPipeline(object):
    def __init__(self):
        self.limit = 50

    def process_item(self, item, spider):
        if item['text']:
            if len(item['text']) > self.limit:
                item['text'] = item['text'][:self.limit].rstrip() + '...'
            return item
        else:
            return DropItem('Missing Text')


class ScrapytutorialPipeline:
    def process_item(self, item, spider):
        return item
