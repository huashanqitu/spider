# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class XicidailiItem(scrapy.Item):
    # 国家
    country=scrapy.Field()
    # IP地址
    ip=scrapy.Field()
    # 端口号
    port=scrapy.Field()
    # 服务器地址
    address=scrapy.Field()
    # 是否匿名
    anonymous=scrapy.Field()
    # 类型
    type=scrapy.Field()
    # 速度
    speed=scrapy.Field()
    # 连接时间
    connect_time=scrapy.Field()
    # 存活时间
    alive_time=scrapy.Field()
    # 验证时间
    verify_time=scrapy.Field()

