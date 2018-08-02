# -*- coding: utf-8 -*-
#基于python3.6
import scrapy
from scrapy.spiders import Spider
from scrapy.http import Request
from scrapy.selector import Selector
from movie.items import MovieItem
from bs4 import BeautifulSoup

class MoviespiderSpider(scrapy.Spider):
    name = "moviespider"
    allowed_domains = ["https://movie.douban.com/"]
    start_urls = ["https://movie.douban.com/top250"]


    def parse(self, response):
        #获取所有的电影链接
        print (response)
        big_urls = response.css('.pic a::attr(href)').extract_first()
        # print (big_urls)
        print (len(big_urls))
        for big_url in big_urls:
            yield Request(big_url,self.parse_two,)

    def pares_two(self,response):
        #
        pass

