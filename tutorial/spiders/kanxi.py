# -*- coding: utf-8 -*-
import scrapy
from scrapy.selector import Selector
from tutorial.items import *


class A33mdSpider(scrapy.Spider):
    name = "33md1"
    allowed_domains = ["kanxi123.com"]
    start_urls = ["http://www.kanxi123.com/sort/movie/"]

    def parse(self, response):
        sel = Selector(response)
        urls = sel.xpath('//div[@class="k_list-index"]/div[@class="k_list-index-1"]/div[@class="k_list-index-1c"]/ul/li[@class="k_list-index-1b-b"]')
        for url in urls:
            url = 'http://www.kanxi123.com' + url.xpath('a/@href').extract()[0]
            yield scrapy.http.Request(url, self.movie_parse)

    def movie_parse(self, response):
        sel = Selector(response)
        url = sel.xpath('//div[@class="k_pape"]/a/@href').extract()
        end_url = url[-2].split('/')[3]
        start_url = url[0][:-2]
        for i in range(1, int(end_url)+1):
            if i == 1:
                parse_url = 'http://www.kanxi123.com' + start_url
            else:
                parse_url = 'http://www.kanxi123.com' + start_url + str(i) + "/"
            yield scrapy.http.Request(parse_url, self.movie_list)

    def movie_list(self,response):
        sel = Selector(response)
        sites = sel.xpath('//div[@id="k_list-lb-2-a"]')
        for site in sites:
            url = 'http://www.kanxi123.com' + site.xpath('a/@href').extract()[0]
            yield scrapy.http.Request(url, self.movie_detail)

    def movie_detail(self, response):
        sel = Selector(response)
        sites = sel.xpath('//div[@class="k_jianjie-3a-7a"]')
        items = []
        urls = sel.xpath('//div[@id="k_jianjie-3a"]/div[@class="k_jianjie-3a-2"]/ul/li[@class="k_jianjie-3a-2b"]')
        for site in sites:
            # item = TestItem()
            # item['name'] = sel.xpath('//li[@class="k_jianjie-3a-1-name"]/text()').extract()[0]
            # item['year'] = sel.xpath('//li[@class="k_jiajie-3a-1-gx"]/a/text()').extract()[0]
            # item['byname'] = urls.xpath('div[@class="k_jianjie-3a-3"]/ul/li[@class="k_jianjie-3a-3b"]/text()').extract()[0]
            #
            # item['director'] = urls.xpath('div[@class="k_jianjie-3a-2"]/ul/li[@class="k_jianjie-3a-2b"]/a/text()').extract()[1]
            #
            # item['area'] = urls.xpath('div[@class="k_jianjie-3a-2"]/ul/li[@class="k_jianjie-3a-2b"]/text()').extract()[2]
            #
            # item['dialogue']= urls.xpath('div[@class="k_jianjie-3a-2"]/ul/li[@class="k_jianjie-3a-2b"]/text()').extract()[3]
            # item['subtitle']= urls.xpath('div[@class="k_jianjie-3a-2"]/ul/li[@class="k_jianjie-3a-2b"]/text()').extract()[4]
            # item['desc'] = urls.xpath('div[@class="k_jianjie-3a-2"]/ul/li[@class="k_jianjie-3a-2b"]/text()').extract()[1]
            # item['type'] = urls.xpath('div[@class="k_jianjie-3a-3"]/ul/li[@class="k_jianjie-3a-3b"]/text()').extract()[1]
            #
            # item['url_title'] = site.xpath['li[@class="k_jianjie-3a-7a-title"]/text()'].extract()[0]
            # item['url'] = site.xpath['li[@class="k_jianjie-3a-7a-link"]/a/href()'].extract()[0]
            # item['url_pass'] = site.xpath['li[@class="k_jianjie-3a-7a-pass"]/text()'].extract()[0]
            # items.append(item)
            item = TestItem()
            item['title'] = sel.xpath('//li[@class="k_jianjie-3a-1-name"]/text()').extract()[0]
            item['year'] = sel.xpath('//li[@class="k_jianjie-3a-1-gx"]/a/text()').extract()[0]
            item['coverlink'] = sel.xpath('//div[@id="k_jianjie-2b"]/a/img/@src').extract()[0]
            item['link'] = response.url
            # item['intro']
            # item['tags']
            # item['actors']
            # item['director']= sel.xpath('//div[@id="k_jianjie-3a"]/div[@class="k_jianjie-3a-2"]/ul/li[@class="k_jianjie-3a-2b"]/a/text()').extract()[0]
            item['director'] = urls[1].xpath('a/text()').extract()[0]
            # item['downloadlink']
            # item['datetime']

            items.append(item)
        return items
