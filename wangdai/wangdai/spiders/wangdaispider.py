# -*- coding: utf-8 -*-
import scrapy
from scrapy.loader import ItemLoader
from wangdai.items import WangdaiItem
from wangdai.items import ChangeItem
import socket
import datetime
import re
import json
class WangdaispiderSpider(scrapy.Spider):
    name = 'wangdaispider'
    allowed_domains = ['p2peye.com']
    start_urls = ['https://www.p2peye.com/platform/all/']

    def parse(self, response):
        url = "https://www.p2peye.com/?platformajax=1&&abbreviations=1"
        yield scrapy.Request(url,self.parse_next)
    def parse_next(self, response):
        js = json.loads(response.text)
        # print(js)
        data=js["data"]
        # print(data)
        for each in data:
            pid = each["p"]
            #print(type(pid))
            d = each['d']
            n = each["n"]
            url = 'https://%s.p2peye.com/beian/' % d
            # print(url)
            header = {'Host': "%s.p2peye.com" % d,
                      "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3",
                      "referer":"https://www.p2peye.com/platform/all"}
            yield scrapy.Request(url, callback=self.parse_items, headers=header,
                                 meta={"d": d,"p": pid,"n":n})
    def parse_items(self,response):
        d = response.meta["d"]
        pid = response.meta["p"]
        n = response.meta["n"]
        l = ItemLoader(item=WangdaiItem(),response=response)
        name = response.xpath('//*[@class="detail"][2]//div[contains(@class,"kv")]//text()').extract()
        l.add_value("name",name)
        company_type = response.xpath('//*[@class="tbl_body"]//div[contains(@class,"tbl_td")]/text()').extract()
        l.add_value('company_type',company_type)
        leading_member = response.xpath('//div[@class="kvs kvs_zyry"]/div[contains(@class,"kv")]/div/@title').extract()
        l.add_value("leading_member",leading_member)
        content = response.xpath('//div[@class="kvs kvs_baxx"]/div//text()').extract()
        l.add_value("content",content)
        l.add_value("title",n)
        l.add_value("project",self.settings.get("BOT_NAME"))
        l.add_value("spider",self.name)
        l.add_value('server',socket.gethostname())
        l.add_value('data', datetime.datetime.now())
        l.add_value("pid",int(pid))
        l.add_value("url",response.url)
        yield l.load_item()
        log_num = response.xpath('//*[@id="tit_BGJL"]/text()').extract()
        if log_num:
            num = int(re.findall("\d+",log_num[0])[0])
            # print(num)
            i = num // 5+(1 if num % 5 else 0 )
            for j in range(1,i+1):
                headers = {"Host": "%s.p2peye.com" % d,
                           "Origin": "https://%s.p2peye.com"% d}
                next_url = "https://%s.p2peye.com/comchanajax/?pid=%s&pn=%s"%(d,pid,str(j))
                yield scrapy.Request(next_url,callback=self.chang_log_item,headers=headers)
    
    def chang_log_item(self,response):
        js = json.loads(response.text)
        item_change = ChangeItem()
        for each in js["data"]["data"]:
            item_change["contentBefore"] = each["contentBefore"].replace("<em>","").replace("</em>","")
            item_change["contentAfter"] = each["contentAfter"].replace("<em>","").replace("</em>","")
            item_change["changeItem"] = each['changeItem']
            item_change["changeTime"] = each["changeTime"]
            item_change["change_pid"] = int(each["pid"])
            yield item_change