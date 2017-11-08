#!/use/bin/env python
#_*_coding:utf-8_*_
import re
import scrapy
from scrapy.http import Request
from tiebaComment.clearDataTool import Tool
from tiebaComment.items import TiebaIdsItem

class MySpider(scrapy.Spider):
    name =  'tiebaComment'
    allowed_domain = ['https://tieba.baidu.com/']
    base_url = r'https://tieba.baidu.com/f?kw=%E6%88%92%E8%B5%8C&ie=utf-8&pn='
    tool = Tool()

    def start_requests(self):
        for i in range(0, 50):
            url = self.bash_url + str(i*50)
            yield Request(url, callback = self.parse)

    def parse(self, response):
        item = TiebaIdsItem()
        pattern1 = re.compile('''<li.*?j_thread_list clearfix.*?data-field='{.*?id&quot;:(.*?),.*?reply_num&quot;:(.*?),.*?}' >''')
        pattern2 = re.compile('<a.*?title="(.*?)".*?class="j_th_tit ".*?>.*?</a>')
        results = re.findall(pattern1, response.text)
        titles = re.findall(pattern2, response.text)
        for result in results:
            item['tid'] = result[0]
            item['replyNums'] = result[1]
        for title in titles:
            item['title'] = title
        return item



