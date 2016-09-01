# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy

##
class TutorialItem(scrapy.Item):
    # define the fields for your item here like:
    title = scrapy.Field()#电影名--
    tags=scrapy.Field()#关键字,标签 可为空
    link=scrapy.Field()#爬虫进入影片详情页面的链接
    intro=scrapy.Field()#包含演员职员表
    year=scrapy.Field()
    actors=scrapy.Field()
    director=scrapy.Field()
    downloadlink=scrapy.Field()#下载链接
    datetime=scrapy.Field()#电影网站上架时间
    coverlink=scrapy.Field()#封面链接
    country=scrapy.Field()
    disc=scrapy.Field()