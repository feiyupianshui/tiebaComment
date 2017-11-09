# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
from pymongo import MongoClient
import datetime

class TiebacommentPipeline(object):

    def __init__(self):
        Client = MongoClient('mongodb://hmq:118667@localhost:27017/')
        db = Client['tiebacomment']
        self.save = db['nogambling']

    def process_item(self, item, spider):
        tid = item['tid']
        replynums = item['replynums']
        title = item['title']
        page = item['page']
        comments = item['comments']
        id = int(tid) + page
        post = {
            '_id': id,
            'tid': tid,
            '标题': title,
            '回复数': replynums,
            '页数': page,
            '评论': comments,
            '存储时间': datetime.datetime.now()
        }
        self.save.insert_one(post)
        return item
