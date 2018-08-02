# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html

import pymongo
import codecs
import os
import re
import urllib
import requests
from PIL import Image
from io import BytesIO

class DoubanPipeline(object):
    '''
    实现保存到txt文件的类，类名这个地方为了区分，做了修改，
    当然这个类名是什么并不重要，你只要能区分就可以，
    请注意，这个类名待会是要写到settings.py文件里面的。
    '''
    def process_item(self, item, spider):
        file_name1 = item['title'] + '  ' + item['jinju']
        file_name1 += ".txt"
        file_name = r'C:\Users\ME\Desktop\Python project\pachong\scrapy\douban\movie'
        # 创建主目录
        if (not os.path.exists(file_name)):
            os.makedirs(file_name)
        filename2 = file_name + '/' + item['title']
        if (not os.path.exists(filename2)):
            os.makedirs(filename2)
        fp = codecs.open(filename2 + '/' + file_name1, 'w')
        fp.write('电影名字：'+ item['title'] + '\n')
        fp.write('公映时间：'+ item['publish_time'] + '\n')
        fp.write('豆瓣评分：'+ item['grade'] + '\n')
        fp.write('豆瓣链接：'+ item['url'] + '\n')
        fp.write('金句：'+ item['jinju'] + '\n')
        fp.write('电影主演：'+ item['actor'] + '\n')
        fp.write('剧情：'+ item['tag'] + '\n')
        fp.write('电影简介：'+ item['content'] + '\n')
        fp.write('大家怎么看：'+ item['duanping'] +'\n')
        fp.write('什么网站可以看：' + '\n' + item['shipinwangzhan'] + '\n')
        fp.close()
        this_url = item['poster']
        response = requests.get(this_url)
        image = Image.open(BytesIO(response.content))
        image.save(filename2 + '/' + item['title'] + '.jpg')
        for i in range(len(item['photo'])):
            photo = item['photo'][i]
            response = requests.get(photo)
            image = Image.open(BytesIO(response.content))
            image.save(filename2 + '/' + str(i) + '.jpg')
        return item


# class MongoPipeline(object):
#     '''
# 	实现保存到mongo数据库的类，
# 	'''
#
#     collection = 'douban'  # mongo数据库的collection名字，随便
#
#     def __init__(self, mongo_uri, mongo_db):
#         self.mongo_uri = mongo_uri
#         self.mongo_db = mongo_db
#
#     @classmethod
#     def from_crawler(cls, crawler):
#         '''
#         scrapy为我们访问settings提供了这样的一个方法，这里，
#         我们需要从settings.py文件中，取得数据库的URI和数据库名称
#         '''
#         return cls(mongo_uri=crawler.settings.get('MONGO_URI'),mongo_db=crawler.settings.get('MONGO_DB'))
#
#     def open_spider(self, spider):  # 爬虫一旦开启，就会实现这个方法，连接到数据库
#         self.client = pymongo.MongoClient(self.mongo_uri)
#         self.db = self.client[self.mongo_db]
#
#     def close_spider(self, spider):  # 爬虫一旦关闭，就会实现这个方法，关闭数据库连接
#         self.client.close()
#
#     def process_item(self, item, spider):
#         '''
#         每个实现保存的类里面必须都要有这个方法，且名字固定，用来具体实现怎么保存
#         '''
#         titles = item['title']
#         links = item['url']
#         table = self.db[self.collection]
#         for i, j in zip(titles, links):
#             data = {}
#             data['文章：链接'] = i + ':' + j
#             table.insert_one(data)
#         return item