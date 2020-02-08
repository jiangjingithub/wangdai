# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
from twisted.enterprise import adbapi
from wangdai.items import WangdaiItem,ChangeItem
from .tools.create_db import PyMysql
class WangdaiPipeline(object):

    def open_spider(self,spider):

        self.dbpool = adbapi.ConnectionPool("pymysql",host="127.0.0.1",port=3306,db="wangdai",user="root",passwd="890311",charset="utf8")

    def process_item(self, item, spider):
        if isinstance(item,WangdaiItem):
            self.dbpool.runInteraction(self.insert_db_content,item)
        elif isinstance(item,ChangeItem):
            self.dbpool.runInteraction(self.insert_db_change,item)
        return item

    def insert_db_content(self,tx,item):

        values = ",".join(["%s"]*len(item))
        keys = ",".join(item.keys())
        sql = "INSERT INTO content ({keys}) VALUES ({values})".format(keys=keys,values=values)
        try:
            tx.execute(sql,tuple(item.values()))
        except Exception as e:
            print(e)
    def insert_db_change(self,tx,item):

        values = ",".join(["%s"]*len(item))
        keys = ",".join(item.keys())
        sql = 'INSERT INTO change_log ({keys}) VALUES ({values})'.format(keys=keys,values=values)
        try:
            tx.execute(sql,tuple(item.values()))
        except Exception as e:
            print(e)
    def close_spider(self,spider):
        self.dbpool.close()