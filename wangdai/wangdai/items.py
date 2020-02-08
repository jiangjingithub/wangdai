# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy
from scrapy.loader.processors import MapCompose,Join,TakeFirst,Identity
from scrapy.loader import ItemLoader

class WangdaiItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    # 公司名
    title = scrapy.Field()
    pid = scrapy.Field()
    name = scrapy.Field(input_processor=MapCompose(str.strip,
                        lambda i: i.replace("\n","")),
                        output_processor=Join())
    company_type = scrapy.Field(input_processor=MapCompose(str.strip),
                                output_processor=Join())
    # 主要成员
    leading_member = scrapy.Field(input_processor=MapCompose(str.strip),
                                output_processor=Join())
    content = scrapy.Field(input_processor=MapCompose(str.strip,lambda i: i.replace("\n","")),
                                output_processor=Join())
    url = scrapy.Field()    
    project = scrapy.Field()
    spider = scrapy.Field()
    server = scrapy.Field()
    data = scrapy.Field()
class ChangeItem(scrapy.Item):
    # 变更记录
    contentBefore = scrapy.Field(input_processor=MapCompose(str.strip))
    contentAfter = scrapy.Field(input_processor=MapCompose(str.strip))
    changeItem = scrapy.Field()
    changeTime = scrapy.Field()
    change_pid = scrapy.Field()