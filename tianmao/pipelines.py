# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
import pymongo


class TianmaoPipeline(object):
    def __init__(self):
        connection = pymongo.MongoClient()
        self.db = connection.taobao
        self.tb = self.db.tmail

    def process_item(self, item, spider):
        self.tb.insert_one(dict(item))
        # return item
