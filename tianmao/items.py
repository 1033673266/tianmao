# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class TianmaoItem(scrapy.Item):
    # define the fields for your item here like:
    type_name = scrapy.Field()
    type_link = scrapy.Field()
    child_type_name = scrapy.Field()
    child_type_link = scrapy.Field()
    name = scrapy.Field()
    price = scrapy.Field()
    sale = scrapy.Field()
    link = scrapy.Field()
