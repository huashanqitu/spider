# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class SpiderBoleBlogItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    pass

# 在Item.py中新建一个JobboleArticleItem类，用来存放文章信息
class JobboleArticleItem(scrapy.Item):
    front_img = scrapy.Field() # 封面图
    title = scrapy.Field()   # 标题
    create_time = scrapy.Field()  # 发布时间
    url = scrapy.Field()  # 当前页url
    article_type =scrapy.Field()  # 文章分类
    praise_number = scrapy.Field() # 点赞数
    collection_number = scrapy.Field() # 收藏数
    comment_number = scrapy.Field() # 评论数

