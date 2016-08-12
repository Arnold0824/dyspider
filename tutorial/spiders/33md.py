# -*- coding: utf-8 -*-
import scrapy
from scrapy.selector import Selector
from tutorial.items import *
from datetime import datetime
import re

class A33mdSpider(scrapy.Spider):
    name = "kanxi"
    allowed_domains = ["kanxi123.com"]
    start_urls = (
        "http://www.kanxi123.com/sort/hd/",
                  )

    def parse(self, response):
        lasttime = '2016-08-05 00:00:00'
        lasttime = datetime.strptime(lasttime, '%Y-%m-%d %H:%M:%S')
        # import re
        pa = re.compile(r'(\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2})')
        i = 0
        for sel in response.css('table td b'):
            item = TutorialItem()
            item['tags'] = sel.xpath('a[1]/text()').extract()[0]
            item['title'] = sel.xpath('a[2]/text()').extract()[0]
            item['link'] = 'http://www.ygdy8.net' + sel.xpath('a[2]/@href').extract()[0]
            try:
                s = response.css('table td font').xpath('text()').extract()[i]
                nowtime = pa.search(s).groups()[0]
            except:
                nowtime = str(datetime.now())
            item['datetime'] = datetime.strptime(nowtime, '%Y-%m-%d %H:%M:%S')
            if item['datetime'] > lasttime:
                res = scrapy.Request(item['link'], self.parse_film_html)
                res.meta['item'] = item
                yield res
            i += 1
        next_page = response.css(
            'html body div#header div.contain div.bd2 div.bd3 div.bd3r div.co_area2 div.co_content8 div.x a::attr("href")')
        if next_page:
            url = response.urljoin(next_page[-2].extract())
            yield scrapy.Request(url, self.parse)

    def parse_film_html(self, response):
        item = response.meta['item']
        item['intro'] = ''.join(response.css('#Zoom p').xpath('text()').extract())
        item['downloadlink'] = response.css('#Zoom a').xpath('text()').extract()[0]
        item['coverlink'] = response.css('#Zoom img::attr("src")').extract()[0]
        yield item
    # def parse(self, response):
    #     urls = response.xpath('//div[@class="k_list-index"]/div[@class="k_list-index-1"]/div[@class="k_list-index-1c"]/ul/li[@class="k_list-index-1b-b"]')
    #     for url in urls:
    #         url = 'http://www.kanxi123.com' + url.xpath('a/@href').extract()[0]
    #         yield scrapy.http.Request(url, self.movie_parse)
    #
    # def movie_parse(self, response):
    #     sel = Selector(response)
    #     url = sel.xpath('//div[@class="k_pape"]/a/@href').extract()
    #     end_url = url[-2].split('/')[3]
    #     start_url = url[0][:-2]
    #     for i in range(1, int(end_url)+1):
    #         if i == 1:
    #             parse_url = 'http://www.kanxi123.com' + start_url
    #         else:
    #             parse_url = 'http://www.kanxi123.com' + start_url + str(i) + "/"
    #         yield scrapy.http.Request(parse_url, self.movie_list)
    #
    # def movie_list(self,response):
    #     sel = Selector(response)
    #     sites = sel.xpath('//div[@id="k_list-lb-2-a"]')
    #     for site in sites:
    #         url = 'http://www.kanxi123.com' + site.xpath('a/@href').extract()[0]
    #         yield scrapy.http.Request(url, self.movie_detail)
    #
    # def movie_detail(self, response):
    #     sel = Selector(response)
    #     sites = sel.xpath('//div[@class="k_jianjie-3a-7a"]')
    #     items = []
    #     urls = sel.xpath('//div[@id="k_jianjie-3a"]/div[@class="k_jianjie-3a-2"]/ul/li[@class="k_jianjie-3a-2b"]')
    #     for site in sites:
    #         # item = TestItem()
    #         # item['name'] = sel.xpath('//li[@class="k_jianjie-3a-1-name"]/text()').extract()[0]
    #         # item['year'] = sel.xpath('//li[@class="k_jiajie-3a-1-gx"]/a/text()').extract()[0]
    #         # item['byname'] = urls.xpath('div[@class="k_jianjie-3a-3"]/ul/li[@class="k_jianjie-3a-3b"]/text()').extract()[0]
    #         #
    #         # item['director'] = urls.xpath('div[@class="k_jianjie-3a-2"]/ul/li[@class="k_jianjie-3a-2b"]/a/text()').extract()[1]
    #         #
    #         # item['area'] = urls.xpath('div[@class="k_jianjie-3a-2"]/ul/li[@class="k_jianjie-3a-2b"]/text()').extract()[2]
    #         #
    #         # item['dialogue']= urls.xpath('div[@class="k_jianjie-3a-2"]/ul/li[@class="k_jianjie-3a-2b"]/text()').extract()[3]
    #         # item['subtitle']= urls.xpath('div[@class="k_jianjie-3a-2"]/ul/li[@class="k_jianjie-3a-2b"]/text()').extract()[4]
    #         # item['desc'] = urls.xpath('div[@class="k_jianjie-3a-2"]/ul/li[@class="k_jianjie-3a-2b"]/text()').extract()[1]
    #         # item['type'] = urls.xpath('div[@class="k_jianjie-3a-3"]/ul/li[@class="k_jianjie-3a-3b"]/text()').extract()[1]
    #         #
    #         # item['url_title'] = site.xpath['li[@class="k_jianjie-3a-7a-title"]/text()'].extract()[0]
    #         # item['url'] = site.xpath['li[@class="k_jianjie-3a-7a-link"]/a/href()'].extract()[0]
    #         # item['url_pass'] = site.xpath['li[@class="k_jianjie-3a-7a-pass"]/text()'].extract()[0]
    #         # items.append(item)
    #         item = TestItem()
    #         item['title'] = sel.xpath('//li[@class="k_jianjie-3a-1-name"]/text()').extract()[0]
    #         item['year'] = sel.xpath('//li[@class="k_jianjie-3a-1-gx"]/a/text()').extract()[0]
    #         item['coverlink'] = sel.xpath('//div[@id="k_jianjie-2b"]/a/img/@src').extract()[0]
    #         item['link'] = response.url
    #         # item['intro']
    #         # item['tags']
    #         # item['actors']
    #         # item['director']= sel.xpath('//div[@id="k_jianjie-3a"]/div[@class="k_jianjie-3a-2"]/ul/li[@class="k_jianjie-3a-2b"]/a/text()').extract()[0]
    #         item['director'] = urls[1].xpath('a/text()').extract()[0]
    #         # item['downloadlink']
    #         # item['datetime']
    #
    #         items.append(item)
    #     return items
