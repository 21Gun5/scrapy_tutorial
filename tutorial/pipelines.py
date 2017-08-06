# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html

import pymongo
import settings

class TutorialPipeline(object):
    def __init__(self):
        host = settings.MONGODB_HOST
        port = settings.MONGODB_PORT
        dbname = settings.MONGODB_DBNAME
        table = settings.MONGODB_TABLE
        client = pymongo.MongoClient(host = host, port = port)
        db = client[dbname]
        self.table = db[table]
    def process_item(self, item, spider):
        quote_info = dict(item)
        self.table.insert(quote_info)
        return item
