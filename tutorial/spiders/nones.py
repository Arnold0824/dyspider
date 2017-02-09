# -*- coding: utf-8 -*-
import scrapy
from scrapy.selector import Selector
from tutorial.items import *
from datetime import datetime,timedelta
import re

class piaohuaSpider(scrapy.Spider):
    name = "piaohua"
    allowed_domains = ["piaohua.com"]
    start_urls = (
        "http://www.piaohua.com/html/dongzuo/list_1.html",
                  )

    def parse(self, response):
        lasttime = '8-17'
        lasttime = datetime.strptime(lasttime, '%m-%d')

        # import re
        pa = re.compile(r'(\d{1,2}-\d{1,2})')
        for sel in response.css('#list dd'):
            item = TutorialItem()
            #item['tags'] = ",".join(sel.css('.k_list-lb-2').xpath('div[4]/a/text()').extract())
            item['title'] = sel.css('#list dd a b font').xpath('text()').extract()
            item['link'] = 'http://www.piaohua.com' + sel.css('a').xpath('@href').extract()[0]
            try:
                s = sel.css('span').xpath('text()').extract()[0]
                nowtime = pa.search(s).groups()[0]
                # print(nowtime)
                thistime = datetime.strptime(nowtime, '%m-%d')
            except:
                #nowtime = str(datetime.now())
                thistime= lasttime
            # yield item

            if thistime > lasttime:
                res = scrapy.Request(item['link'], self.parse_film_html)
                res.meta['item'] = item
                yield res
        next_page = response.css('div.page a::attr("href")')
        if next_page:
            url = response.urljoin(next_page.extract()[-2])
            yield scrapy.Request(url, self.parse)

    def parse_film_html(self, response):
        pa = re.compile(r'(\d{4}-\d{1,2}-\d{1,2})')
        item = response.meta['item']
        a={}
        s = ''.join(response.css('#showinfo').xpath('div/text()').extract()).replace('\u3000', '').replace('\n', '').replace('\t', '').replace('\r', '').split('◎')
        for x in s:
            a[x[:2]] = x[2:]
        try:
            try:
                item['director']=a['导演']
            except:
                item['director']='暂无'
            try:
                item['intro']=a['简介']
            except:
                item['intro']=['内容']
            item['coverlink']=response.css('#showinfo img').xpath('@src').extract()[0]
            item['actors']=a['主演']
            item['year']=a['年代']
            try:
                item['datetime']=datetime.strptime(pa.search(a['上映']).groups()[0],'%Y-%m-%d')     #a['上映'][2:] if a['上映']!='' else a['年代']+
            except:
                item['datetime']=datetime.now()
            item['downloadlink']="\n".join(response.css('table a').xpath('@href').extract())+' \n'#+"\n".join(response.css('.k_jianjie-3a-7a-pass').xpath('text()').extract())
            item['country']=a['国家']
            item['tags']=a['类别']
            try:
                item['disc']="IM"+a['IM']+a['豆瓣']
            except:
                pass
        except:
            item['intro']='\n'.join(response.css("#showinfo").extract())
        # try:
        #     item['intro']+=''
        # except:
        #     pass
        yield item
