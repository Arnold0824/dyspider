# -*- coding: utf-8 -*-
import scrapy
from tutorial.items import TutorialItem
from datetime import datetime
import re

class DySpider(scrapy.Spider):
    name = "dy"
    allowed_domains = ["ygdy8.net"]
    start_urls = (
        'http://www.ygdy8.net/html/gndy/oumei/index.html',
        'http://www.ygdy8.net/html/gndy/china/index.html',
        'http://www.ygdy8.net/html/gndy/dyzz/index.html',
    )

    def parse(self, response):
        lasttime = '1990-08-05 00:00:00'
        lasttime=datetime.strptime(lasttime, '%Y-%m-%d %H:%M:%S')
        #import re
        pa = re.compile(r'(\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2})')
        i=0
        for sel in response.css('table td b'):
            item=TutorialItem()
            #item['tags']=sel.xpath('a[1]/text()').extract()[0]
            title=sel.xpath('a[2]/text()').extract()[0]
            try:
                item['title'] = re.compile(r'《(.*)》').search(title).groups()[0].split('/')[0]
            except:
                item['title']= title
            item['link']='http://www.ygdy8.net'+sel.xpath('a[2]/@href').extract()[0]
            try:
                s = response.css('table td font').xpath('text()').extract()[i]
                nowtime=pa.search(s).groups()[0]
            except:
                nowtime=str(datetime.now())
            item['datetime']=datetime.strptime(nowtime,'%Y-%m-%d %H:%M:%S')
            #if item['datetime']>lasttime:
            res=scrapy.Request(item['link'], self.parse_film_html)
            res.meta['item']=item
            yield res
            i+=1

        next_page=response.css('html body div#header div.contain div.bd2 div.bd3 div.bd3r div.co_area2 div.co_content8 div.x a::attr("href")')
        try:
            depth=int(next_page.extract()[-2][-6])-1
        except:
            depth=1
        if next_page and depth<2:
            url=response.urljoin(next_page[-2].extract())
            yield scrapy.Request(url,self.parse)
    def parse_film_html(self,response):
        item=response.meta['item']
        all_intro_text=''.join(response.css('#Zoom p').xpath('text()').extract()).replace('\u3000','')
        #s=pa.search(a).groups()[0]
        try:
            item['tags']=re.compile(r'◎类别(.+?)◎').search(all_intro_text).groups()[0].replace('/',',')
        except:
            item['tags']='动作'
        # try:
        #     item['title']=re.compile(r'◎译名(.+?)◎').search(all_intro_text).groups()[0].split('/')[0]
        # except:
        #     pass
        try:
            item['intro']=re.compile(r'◎简介(.+)').search(all_intro_text).groups()[0]
        except:
            item['intro'] ='暂无介绍'
        # try:
        #     item['intro']+=re.compile(r'◎译名(.+?)◎').search(all_intro_text).groups()[0]
        # except:
        #     pass
        try:
            item['director']=re.compile(r'◎导演(.+?)◎').search(all_intro_text).groups()[0]
        except:
            item['director'] ='暂无'
        try:
            item['country'] = re.compile(r'◎国家(.+?)◎').search(all_intro_text).groups()[0]
        except:
            item['country'] = '暂无'
        try:
            item['actors'] = re.compile(r'◎主演(.+?)◎').search(all_intro_text).groups()[0]
        except:
            item['actors'] = '暂无'
        try:
            item['year'] = re.compile(r'◎年代(.+?)◎').search(all_intro_text).groups()[0]
        except:
            item['year'] = '暂无'
        item['downloadlink']=response.css('#Zoom a').xpath('text()').extract()[0]
        item['coverlink']=response.css('#Zoom img::attr("src")').extract()[0]
        yield item