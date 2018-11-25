# -*- coding: utf-8 -*-
import scrapy
import re
# 发送请求爬取页面
from scrapy.http import Request
# 归正url
from urllib import parse
from ..items import JobboleArticleItem


# 爬虫类

class JobboleSpider(scrapy.Spider):
    name = 'jobbole'
    allowed_domains = ['blog.jobbole.com']
    start_urls = ['http://blog.jobbole.com/all-posts/']

    # //*[@id="post-114256"]/div[1]/h1
    # 
    # scrapy 的 response里面包含了xpath方法，可以直接用调用，返回值为Selector类型
    # Selector库中有个方法extract(),可以获取到data数据
    def parse(self, response):
        # 1.获取单页面a标签内容，返回Selector对象
        post_urls = response.xpath('//*[@id="archive"]/div/div[1]/a')
        # 2.获取文章url、封面图url、下载页面内容和图片
        for post_node in post_urls:
            # 2.1 获取单页面文章url
            image_url = post_node.css("img::attr(src)").extract_first("")
            # 2.2 获取单页面文章url
            post_url = post_node.css("::attr(href)").extract_first("")
            # 2.3 提交下载
            yield Request(url=parse.urljoin(response.url, post_url), meta={"front_img": image_url},
                          callback=self.parse_detail)
        # 3.获取翻页url和翻页下载
        next_url = response.css(".next::attr(href)").extract()
        if next_url != []:
            next_url = next_url[0]
            yield Request(url=parse.urljoin(response.url, next_url), callback=self.parse)

    # 获取单篇文章详情信息
    def parse_detail(self, response):
        # 文章标题
        # //*[@id]/div[1]/h1
        title = response.xpath('//*[@id]/div[1]/h1/text()').extract()[0]

        # 发布日期
        data_r = response.css(".entry-meta-hide-on-mobile::text").extract()[0].strip()
        create_time = data_r.replace('·', '').strip()

        # 文章分类
        article_type = response.css("p.entry-meta-hide-on-mobile a::text").extract()
        if article_type != []:
            article_type = ",".join(article_type)

        # 点赞数
        praise_number = response.css(".href-style.vote-post-up h10::text").extract()
        if praise_number != []:
            praise_number = int(praise_number[0])
        else:
            praise_number = 0

        # 收藏数
        collection_str = response.css("span.btn-bluet-bigger:nth-child(2)::text").extract()[0]
        reg_02 = '.*?(\d+).*'
        collection_number = re.findall(reg_02, collection_str)
        if collection_number:
            collection_number = int(collection_number[0])
        else:
            collection_number = 0

        # 评论数
        comment_number = response.css("a[href='#article-comment'] span::text").extract()[0]
        comment_number = re.findall(reg_02, comment_number)
        if comment_number:
            comment_number = int(comment_number[0])
        else:
            comment_number = 0

        # print("文章标题："+title)
        # print("发布日期："+create_time)
        # print("文章分类："+article_type)
        # print("点赞数："+str(praise_number))
        # print("收藏数："+str(collection_number))
        # print("评论数："+str(comment_number))
        # print("----------------------------------------")

        # 初始化一个item对象
        article_item = JobboleArticleItem()
        # 文章封面图
        front_img = response.meta.get("front_img", "")
        # 数据存储到Item中
        article_item['title'] = title
        article_item['create_time'] = create_time
        article_item['article_type'] = article_type
        article_item['praise_number'] = praise_number
        article_item['collection_number'] = collection_number
        article_item['comment_number'] = comment_number
        article_item['front_img'] = front_img
        article_item['url'] = response.url
        # 将item传递到Pipeline中
        yield article_item
