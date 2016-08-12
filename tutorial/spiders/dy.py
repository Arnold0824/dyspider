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
    )

    def parse(self, response):
        lasttime = '2016-08-05 00:00:00'
        lasttime=datetime.strptime(lasttime, '%Y-%m-%d %H:%M:%S')
        #import re
        pa = re.compile(r'(\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2})')
        i=0
        for sel in response.css('table td b'):
            item=TutorialItem()
            item['tags']=sel.xpath('a[1]/text()').extract()[0]
            item['title']=sel.xpath('a[2]/text()').extract()[0]
            item['link']='http://www.ygdy8.net'+sel.xpath('a[2]/@href').extract()[0]
            try:
                s = response.css('table td font').xpath('text()').extract()[i]
                nowtime=pa.search(s).groups()[0]
            except:
                nowtime=str(datetime.now())
            item['datetime']=datetime.strptime(nowtime,'%Y-%m-%d %H:%M:%S')
            if item['datetime']>lasttime:
                res=scrapy.Request(item['link'], self.parse_film_html)
                res.meta['item']=item
                yield res
            i+=1
        next_page=response.css('html body div#header div.contain div.bd2 div.bd3 div.bd3r div.co_area2 div.co_content8 div.x a::attr("href")')
        if next_page:
            url=response.urljoin(next_page[-2].extract())
            yield scrapy.Request(url,self.parse)
    def parse_film_html(self,response):
        item=response.meta['item']
        item['intro']=''.join(response.css('#Zoom p').xpath('text()').extract())
        item['downloadlink']=response.css('#Zoom a').xpath('text()').extract()[0]
        item['coverlink']=response.css('#Zoom img::attr("src")').extract()[0]
        yield item