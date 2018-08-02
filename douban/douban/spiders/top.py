# -*- coding: utf-8 -*-
import scrapy
from scrapy.http import Request
from douban.items import DoubanItem
import sys
reload(sys)
sys.setdefaultencoding("utf-8")

class TopSpider(scrapy.Spider):
    name = "top"
    allowed_domains = ["https://movie.douban.com/"]
    start_urls = ["https://movie.douban.com/top250"]

    def parse(self, response):
        # for sel in response.xpath('//div[@class="info"]'):
            # item = DmozItem()
            # title = sel.xpath('div[@class="hd"]/a/span/text()').extract()[0]  # 不加[0]会变成Unicode形式
            # star = sel.xpath('div[@class="bd"]/div[@class="star"]/span[@class="rating_num"]/text()').extract()[0]
            # print star, title
        #获得所有的页面
        for i in range(0,250,25):
            # print i
            url = 'https://movie.douban.com/top250?start=' + str(i) + '&filter='
            # print url
            yield Request(url=url,callback=self.parse_two, dont_filter=True)

    def parse_two(self,response):
        #获得所有页面的所有链接
        big_urls = response.css('.pic a::attr(href)').extract()
        # print (big_urls)
        # print (len(big_urls))
        jinju = response.css('.inq::text').extract()
        # print len(jinju)
        for i in range(len(jinju)):
            # print big_url
            big_url = big_urls[i]
            jinju1 = jinju[i]
            yield Request(big_url, self.parse_three,meta = {'jinju':jinju1,'url':big_url},dont_filter=True)

    def parse_three(self,response):
        #获取所有链接的所要爬取的内容
        jinju = response.meta['jinju']
        url = response.meta['url']
        print jinju
        print url

        #获得电影名
        title = response.css('h1 span::text').extract_first()
        print title

        #获得电影公布时间
        publish_time =response.css('h1 span::text').extract()[1]
        print publish_time

        #获得电影评分
        grade = response.css('strong::text').extract_first()
        print grade

        #获得主演
        a=[]
        b = response.css('.actor a::text').extract()
        for d in range(len(b)):
            a.append(b[d])
        # print a
        actor = ','.join(a)
        print actor

        #获得标签
        c = []
        tags = response.css('span[property="v:genre"]::text').extract()
        for e in range(len(tags)):
            c.append(tags[e])
        tag = ','.join(c)
        print tag

        #获得剧情简介
        f = []
        content = response.css('span[property="v:summary"]::text').extract()
        for cc in range(len(content)):
            f.append(content[cc])
        content = ' '.join(f)
        print content

        #获得前五短评
        dd = []
        fifth = response.css('.comment p::text').extract()
        # print len(duanping)
        for i in range(len(fifth)):
            dd.append(fifth[i])
            duanping='\n'.join(dd)

        #获得海报
        poster = response.css('.nbgnbg img::attr(src)').extract_first()
        print poster

        #获得一些剧照
        photos = response.css('.related-pic-bd li a img::attr(src)').extract()
        for photo in photos:
            print photo

        #在哪里可以看这些电影
        g =[]
        shipinwangzhans = response.css('.bs li a::text').extract()
        if shipinwangzhans == None:
            print 'none'
        else:
            for h in range(len(shipinwangzhans)):
                g.append(shipinwangzhans[h])
            shipinwangzhan = ''.join(g)
            print shipinwangzhan


        # 将我们导入的item文件进行实例化，用来存储我们的数据。
        item = DoubanItem()
        item['title'] = title
        item['publish_time'] = publish_time
        item['grade'] = grade
        item['url'] = url
        item['jinju'] = jinju
        item['actor'] = actor
        item['tag'] = tag
        item['content'] = content
        item['duanping'] = duanping
        item['poster'] = poster
        item['photo'] = photos
        item['shipinwangzhan'] = shipinwangzhan

        yield item
