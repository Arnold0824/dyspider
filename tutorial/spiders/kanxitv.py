# -*- coding: utf-8 -*-
import scrapy
from scrapy.selector import Selector
from tutorial.items import *
from datetime import datetime
import re
class A33mdSpider(scrapy.Spider):
    name = "kanxitv"
    # depth = 0
    allowed_domains = ["kanxi.cc"]
    start_urls = (
        "http://www.kanxi.cc/sort/11/",
        "http://www.kanxi.cc/sort/8/",
        "http://www.kanxi.cc/sort/9/",
        "http://www.kanxi.cc/sort/10/",
        "http://www.kanxi.cc/sort/comic/",
        "http://www.kanxi.cc/sort/variety/",
                  )

    def parse(self, response):

        # lasttime = '1900-8-17 4:38:54'
        # lasttime = datetime.strptime(lasttime, '%Y-%m-%d %H:%M:%S')
        # import re
        pa = re.compile(r'(\d{4}-\d{1,2}-\d{1,2} \d{1,2}:\d{1,2}:\d{1,2})')
        for sel in response.css('.k_list-lb'):
            item = TutorialItem()
            item['tags'] = " ".join(sel.css('.k_list-lb-2').xpath('div[4]/a/text()').extract())
            item['title'] = sel.css('.k_list-lb-2').xpath('div[1]/a/text()').extract()[0].replace(' ','')
            try:
                item['year'] = sel.css('.k_list-lb-2').xpath('div[2]/a/text()').extract()[0]
            except:
                item['year'] = sel.css('.k_list-lb-2').xpath('div[2]/span/text()').extract()[0]
            item['link'] = 'http://www.kanxi.cc' + sel.css('.k_list-lb-2').xpath('div[1]/a[1]/@href').extract()[0]
            try:
                s = sel.css('#k_list-lb-2-f').xpath('text()').extract()[0]
                if len(s) > 4:
                    nowtime = pa.search(s).groups()[0]
                    # print(nowtime)
                    item['datetime'] = datetime.strptime(nowtime, '%Y-%m-%d %H:%M:%S')
                else:
                    nowtime = str(datetime.now())
                    item['datetime'] = datetime.strptime(nowtime, '%Y-%m-%d %H:%M:%S')
            except:
                nowtime = str(datetime.now())
                item['datetime'] = datetime.strptime(nowtime, '%Y-%m-%d %H:%M:%S')
            res = scrapy.Request(item['link'], self.parse_film_html)
            res.meta['item'] = item
            yield res
        next_page = response.css('div.k_pape a')[-1]
        try:
            depth=int(next_page.xpath('@href').extract()[0][-2])
        except:
            depth=1
        if next_page.xpath('text()').extract()[0]=='下一页' and depth<5:# and self.depth <50:
            url = response.urljoin(next_page.xpath('@href').extract()[0])
            yield scrapy.Request(url, self.parse)

    def parse_film_html(self, response):
        item = response.meta['item']
        item['director']=response.css('.k_jianjie-3a-2b a').xpath('text()').extract()[-1]
        try:
            item['intro']=response.css('#link-report').xpath('text()').extract()[-1]
        except:
            item['intro']=response.css('#link-report span').xpath('text()').extract()[-1]
        item['coverlink']=response.css('#k_jianjie-2b a img').xpath('@src').extract()[0]
        item['actors']=','.join(response.css('.k_jianjie-3a-3b a').xpath('text()').extract())
        s=""
        try:
            for sel in response.css('.k_jianjie-3a-7a'):
                if('http://pan.' in sel.css('.k_jianjie-3a-7a-link a').xpath('text()').extract()[0]):
                    s+=sel.css('.k_jianjie-3a-7a-link a').xpath('@href').extract()[0] + ',' + sel.css('.k_jianjie-3a-7a-pass').xpath('text()').extract()[0]+'\n'
                else:
                    s += sel.css('.k_jianjie-3a-7a-link a').xpath('@href').extract()[0] + ',' + sel.css('.k_jianjie-3a-7a-link a').xpath('text()').extract()[0]+'\n'
        #[x.split(',') for x in s.split('\n')]  分离
            item['downloadlink']=s
        except:
            item['downloadlink']=" \n"
            #item['downloadlink']="\n".join(response.css('.k_jianjie-3a-7a-link a').xpath('@href').extract())+' \n'+"\n".join(response.css('.k_jianjie-3a-7a-pass').xpath('text()').extract())
        item['country']=response.css('.k_jianjie-3a-2b').xpath('text()').extract()[0]
        yield item
