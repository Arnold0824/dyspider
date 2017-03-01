# -*- coding: utf-8 -*-
import scrapy
from scrapy.selector import Selector
from tutorial.items import *
from datetime import datetime
import re
class btbtdytvSpider(scrapy.Spider):
    name = "bttv"
    depth = 0
    allowed_domains = ["btbtdy.com"]
    start_urls = (
        "http://www.btbtdy.com/screen/30-----time-1.html",
        "http://www.btbtdy.com/screen/34-----time-1.html",

                  )

    def parse(self, response):

        # lasttime = '1900-8-17 4:38:54'
        # lasttime = datetime.strptime(lasttime, '%Y-%m-%d %H:%M:%S')
        # import re
        pa = re.compile(r'(\d{4}-\d{1,2}-\d{1,2} \d{1,2}:\d{1,2}:\d{1,2})')
        for sel in response.css('div.list_lis.list_su dl'):
            item = TutorialItem()
            try:
                item['title'] = sel.css('dt a::attr("title")').extract()[0].replace(' ','')
            except:
                item['title'] = sel.css('dd p.title a').xpath('text()').extract()[0].replace(' ', '')
            item['coverlink']=sel.css('dt a img::attr("data-src")').extract()[0]
            item['link'] = 'http://www.btbtdy.com' + sel.css('dt a::attr("href")').extract()[0]

            try:
                item['country'] = sel.css('dd p.des').xpath('text()').extract()[0].split(' ')[1]
            except:
                item['country'] = '绝对领域'
            res = scrapy.Request(item['link'], self.parse_film_html)
            res.meta['item'] = item
            yield res
        next_page = response.css('div.pages a')[-2]
        try:
            depth=int(response.css('div.pages em').xpath('text()').extract()[0])
        except:
            depth=1
        if next_page.xpath('text()').extract()[0]=='下一页'  and depth<5:# and self.depth <50:
            url = response.urljoin(next_page.xpath('@href').extract()[0])
            yield scrapy.Request(url, self.parse)

    def parse_film_html(self, response):
        item = response.meta['item']
        item['director']='暂无'
        try:
            s = response.css('dd').xpath('text()').extract()[0]
            if len(s) > 4:
                # nowtime = pa.search(s).groups()[0]
                # print(nowtime)
                item['datetime'] = s
            else:
                nowtime = str(datetime.now())
                item['datetime'] = datetime.strptime(nowtime, '%Y-%m-%d %H:%M:%S')
        except:
            nowtime = str(datetime.now())
            item['datetime'] = datetime.strptime(nowtime, '%Y-%m-%d %H:%M:%S')
        try:
            item['tags'] = " ".join(response.css('dd')[2].css('a').xpath('text()').extract())
        except:
            item['tags'] = '动作'
        try:
            item['year'] =  response.css('span.year').xpath('text()').extract()[0].replace('(','').replace(')','').replace(' ','')
        except:
            item['year'] = 'unknown'
        try:
            item['actors'] = ",".join(response.css('dd.zhuyan a').xpath('text()').extract())
        except:
            item['actors'] ='不清楚'

        try:
            item['intro']="".join(response.css('div.des div p').xpath('text()').extract())
            if item['intro']=='':
                item['intro'] = "".join(response.css('div.des div div').xpath('text()').extract())
        except:
            item['intro']="暂无"

        s = ""
        try:
            for sel in response.css('ul.p_list_02 li'):
                s += sel.css('span a::attr(href)').extract()[0] + ',' + \
                     '【dyhell电影网】-'+sel.css('a::attr(title)').extract()[0] + '\n'
                    # [x.split(',') for x in s.split('\n')]  分离
            item['downloadlink'] = s
        except:
            item['downloadlink'] = " \n"

        yield item
