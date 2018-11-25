# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
import pymysql


class SpiderBoleBlogPipeline(object):
    def process_item(self, item, spider):
        return item


class MysqlPipeline(object):
    def __init__(self):
        # 数据库连接
        self.conn = pymysql.connect(host="localhost", port=3306, user="root", password="sunck", charset="utf8",
                                    database="bole")
        self.cur = self.conn.cursor()

    # 插入数据
    def sql_insert(self, sql):
        self.cur.execute(sql)
        self.conn.commit()

    def process_item(self, item, spider):
        # 存入mysql数据库
        sql_word = "insert into article (title,create_time,article_type,praise_number,collection_number,comment_number,url,front_img) values ('{0}','{1}','{2}','{3}','{4}','{5}','{6}','{7}')".format(
            item["title"], item["create_time"], item["article_type"], item["praise_number"], item["collection_number"],
            item["comment_number"], item["url"], item["front_img"])
        self.sql_insert(sql_word)
        return item
