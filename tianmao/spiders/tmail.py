# -*- coding: utf-8 -*-
import scrapy
from scrapy.selector import Selector
from scrapy.http import Request
from ..items import TianmaoItem


class TmailSpider(scrapy.Spider):
    name = 'tmail'
    # allowed_domains = ['www.tmall.com']
    start_urls = ['https://www.tmall.com/']

    def parse(self, response):
        parse_list = ['女鞋']
        selector = Selector(response)
        types = selector.xpath('//*[@id="content"]/div[2]/div[1]/div[3]/div/ul/li/a[1]')
        for father_type in types:
            type_name = father_type.xpath('./text()').extract()[0]
            type_link = father_type.xpath('./@href').extract()[0]
            item = TianmaoItem()
            item['type_name'] = type_name
            item['type_link'] = type_link
            if not type_link:
                continue

            url = 'https:%s' % type_link
            if type_name in parse_list:
                yield Request(url, callback=self.parse_type, meta={'item': item})

    def parse_type(self, response):
        item = response.meta['item']
        selector = Selector(response)
        child_types = selector.xpath('//*[@id="first-screen"]/div[2]/div[1]/div/ul/li/a')
        print('%s: %s' % (item['type_name'], len(child_types)))
        for child_type in child_types:
            try:
                child_type_name = child_type.xpath('./text()').extract()[0]
                child_type_link = child_type.xpath('./@href').extract()[0]
            except:
                continue
            item['child_type_name'] = child_type_name
            item['child_type_link'] = child_type_link
            if not child_type_link:
                continue
            url = 'http:%s' % child_type_link
            yield Request(url, callback=self.parse_content, meta={'item':item})

    def parse_content(self, response):
        item = response.meta['item']
        selector = Selector(response)
        articles = selector.xpath('//*[@id="J_ItemList"]/div/div')
        for article in articles:
            try:
                link = article.xpath('./p[2]/a[1]/@href').extract()[0]
                name = article.xpath('./p[2]/a[1]/text()').extract()[0]
                price = article.xpath('./p[1]/em[1]/text()').extract()[0]
                sale = article.xpath('./p[3]//em[1]/text()').extract()[0]
            except:
                continue
            item['link'] = link
            item['name'] = name
            item['price'] = price
            item['sale'] = sale
            yield item
        try:
            next_page = selector.xpath('//*[@id="content"]/div/div[8]/div/b[1]/a[3]').extract()[0]
        except Exception as e:
            print(e)
            next_page = None
        if next_page:
            url = 'https:%s' % next_page
            yield Request(url=url, callback=self.parse_content, meta={'item':item})