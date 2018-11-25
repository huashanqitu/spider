# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
import pymysql

class XicidailiPipeline(object):
    def __init__(self):
        self.connection = pymysql.connect(host='localhost',
                                          user='root',
                                          password='sunck',
                                          db='daili',
                                          charset='utf8',  # 不能用utf-8
                                          cursorclass=pymysql.cursors.DictCursor)

    def process_item(self, item, spider):
        with self.connection.cursor() as cursor:
            sql = 'insert into xicidaili' \
                  '(country,ip,port,address,anonymous,type,speed,connect_time,alive_time,verify_time) values' \
                  '(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s);'
            args = (
            item['country'], item['ip'], item['port'], item['address'], item['anonymous'], item['type'], item['speed'],
            item['connect_time'], item['alive_time'], item['verify_time'])

            spider.logger.info(args)

            cursor.execute(sql, args)
        self.connection.commit()

    def close_spider(self, spider):
        self.connection.close()

