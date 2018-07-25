# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html

from openpyxl import Workbook

class ScrapyTaobaoPipeline(object):

    #初始化打开一个Workbook
    def __init__(self):
        self.wb = Workbook()
        self.ws = self.wb.active
        self.ws.append(['商品名','销量','商品类型','评论','评论日期','追评'])    #写下表格第一行说明

    #每获得一个item则写一行数据进入表格中
    def process_item(self, item, spider):
        self.ws.append([item['name'],item['sales'],item['comment']['auctionSku'],item['comment']['rateContent'],item['comment']['rateDate'],item['comment']['appendComment']])
        return item

    #爬虫关闭时，保存好表格内数据
    def close_spider(self,spider):
        self.wb.save('comment.xlsx')
