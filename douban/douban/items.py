# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class DoubanItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    title = scrapy.Field()  # 用来存储豆瓣电影标题
    publish_time = scrapy.Field()  # 用来存储豆瓣电影评分
    grade = scrapy.Field()
    url = scrapy.Field()
    jinju = scrapy.Field()
    actor = scrapy.Field()
    tag = scrapy.Field()
    content = scrapy.Field()
    duanping = scrapy.Field()
    poster = scrapy.Field()
    photo = scrapy.Field()
    shipinwangzhan = scrapy.Field()