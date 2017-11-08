# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class TiebaUrlsItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    tid = scrapy.Field()
    replyNums = scrapy.Field()
    title = scrapy.Field()

class TiebacommmentItem(scrapy.Item):
    pages = scrapy.Field()
    comments = scrapy.Field()