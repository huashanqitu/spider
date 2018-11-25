import scrapy
from ..items import XicidailiItem
import time

class XicidailiSpider(scrapy.Spider):
    name = 'xicidaili'
    allowed_domains=['www.xicidaili.com']
    # start_urls=['http://www.xicidaili.com/nn/1']

    def start_requests(self):
        urls=[]
        for i in range(1,11):
            urls.append('http://www.xicidaili.com/nn/'+str(i))
        for url in urls:
            time.sleep(1)
            yield scrapy.Request(url,callback=self.parse,method='GET')

    def parse(self, response):
        tr_list=response.xpath('//table[@id="ip_list"]/tr')
        for tr in tr_list[1:]:  # 过滤掉表头行
            item=XicidailiItem()
            item['country']=tr.xpath('./td[1]/img/@alt').extract_first()
            item['ip']=tr.xpath('./td[2]/text()').extract_first()
            item['port']=tr.xpath('./td[3]/text()').extract_first()
            item['address']=tr.xpath('./td[4]/a/text()').extract_first()
            item['anonymous']=tr.xpath('./td[5]/text()').extract_first()
            item['type']=tr.xpath('./td[6]/text()').extract_first()
            item['speed']=tr.xpath('./td[7]/div/@title').re(r'\d{1,3}\.\d{0,}')[0]
            item['connect_time']=tr.xpath('./td[8]/div/@title').re(r'\d{1,3}\.\d{0,}')[0]
            item['alive_time']=tr.xpath('./td[9]/text()').extract_first()
            item['verify_time']=tr.xpath('./td[10]/text()').extract_first()

            yield item