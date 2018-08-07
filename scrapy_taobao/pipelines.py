# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html

from openpyxl import Workbook
import pymysql
import logging

class ExcelPipeline(object):

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


class MysqlPipeline(object):

    def __init__(self):
        self.db = pymysql.Connect(host='localhost',port=3306,user='root',password='ROOKIE',db='tb_comment',charset='utf8mb4')
        self.cursor = self.db.cursor()
        self.count_goods = 0
        sql1 = """
                CREATE TABLE IF NOT EXISTS goods(
                    id int unsigned NOT NULL AUTO_INCREMENT PRIMARY KEY,
                    good_id bigint unsigned NOT NULL UNIQUE, 
                    good_name char(100) NOT NULL
                );
               """
        sql2 = """
                CREATE TABLE IF NOT EXISTS comments(
                   id int unsigned NOT NULL AUTO_INCREMENT PRIMARY KEY,
                   good_id bigint unsigned unsigned NOT NULL,
                   content text NOT NULL,
                   rate_date timestamp NOT NULL,
                   good_type char(50) NOT NULL,
                   add_comment varchar(255) NULL,
                   CONSTRAINT fk_gc foreign key(good_id) references goods(good_id)
                );
               """
        try:
            self.cursor.execute(sql1)
            self.db.commit()
            print('建表goods...')
        except:
            self.db.rollback()

        try:
            self.cursor.execute(sql2)
            self.db.commit()
            print('建表comments...')
        except:
            self.db.rollback()

    def close_spider(self,spider):
        self.db.close()

    def process_item(self,item,spider):
        good_id = item['itemId']
        good_name = item['name']
        content = item['comment']['rateContent']
        good_type = item['comment']['auctionSku']
        rate_date = item['comment']['rateDate']
        try:
            add_comment = item['comment']['appComment']['content']
        except:
            add_comment =''


        #检测goods表是否已存如该商品
        sql1 ="SELECT good_id FROM goods WHERE good_id=%s;"%(good_id)

        #若goods表还没有该商品记录，写入goods表
        sql2 = "INSERT INTO goods(good_id,good_name) values(%s,'%s'); "%(good_id,good_name)

        #评论信息写入comments表
        sql3 = "INSERT INTO comments(good_id,content,rate_date,good_type,add_comment) values(%s,'%s','%s','%s','%s');"%(good_id,content,rate_date,good_type,add_comment)

        self.cursor.execute(sql1)

        if not self.cursor.fetchone():
            try:
                self.cursor.execute(sql2)
                self.db.commit()
                self.count_goods+=1
                print('写入第%d个商品成功:%s'%(self.count_goods,good_id))
            except:
                self.db.rollback()
                print('写入goods表失败，商品名:%s'%(good_name))
        try:
            self.cursor.execute(sql3)
            self.db.commit()
        except:
            self.db.rollback()
        return item
