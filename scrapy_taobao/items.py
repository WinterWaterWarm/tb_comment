# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class ScrapyTaobaoItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    pass

class taobao_comment_item(scrapy.Item):
    name = scrapy.Field()       #商品名称
    comment = scrapy.Field()    #评论（包含商品类型、评论内容、评论时间、追评的一个字典）
    sales = scrapy.Field()      #销量
    itemId = scrapy.Field()     #商品id
    count = scrapy.Field()      #商品标记，方便调试
    url = scrapy.Field()        #商品链接

