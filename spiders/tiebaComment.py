#!/use/bin/env python
#_*_coding:utf-8_*_
import re
import scrapy
from scrapy.http import Request
from tiebaComment.clearDataTool import Tool
from tiebaComment.items import TiebacommmentItem

class MySpider(scrapy.Spider):
    name =  'tiebaComment'
    allowed_domain = ['https://tieba.baidu.com/']
    base_url = r'https://tieba.baidu.com/f?kw=%E6%88%92%E8%B5%8C&ie=utf-8&pn='
    URL = 'https://tieba.baidu.com/p/'

    def start_requests(self):
        for i in range(0, 50):
            url = self.base_url + str(i*50)
            yield Request(url, callback=self.parse)

    def parse(self, response):
        pattern1 = re.compile('''<li.*?j_thread_list clearfix.*?data-field='{.*?id&quot;:(.*?),.*?reply_num&quot;:(.*?),.*?}' >''')
        results = re.findall(pattern1, response.text)
        for result in results:
            tid = result[0]
            replynums = int(result[1])
            detail_url = self.URL + tid + '?pn=1'
            yield Request(detail_url, callback=self.get_pages, meta={'tid': tid, 'replynums': replynums})

    def get_pages(self, response):
        pattern2 = re.compile('<span class="red">(.*?)</span>')
        try:
            page_num = re.search(pattern2, response.text).group(1)
        except:
            print('帖子不存在，跳过')
        pattern3 = re.compile('<h3 class="core_title_txt pull-left text-overflow  ".*?>(.*?)</h3>')
        try:
            title = re.search(pattern3, response.text).group(1)
        except:
            title = '百度贴吧'
        nowpage = 0
        for x in range(1, int(page_num)+1):
            turn_url = self.URL + response.meta['tid'] + '?pn=' + str(x)
            page = nowpage
            nowpage += 1
            yield Request(turn_url, callback=self.get_comments, meta={'tid': response.meta['tid'], 'replynums': response.meta['replynums'], 'title': title, 'page': page})

    def get_comments(self, response):
        item = TiebacommmentItem()
        tool = Tool()
        partten4 = re.compile('<div.*?class="d_post_content j_d_post_content ">(.*?)</div>')
        commentlist = re.findall(partten4, response.text)
        commentstr = " ".join(commentlist)
        comments = tool.replace(commentstr)
        item['tid'] = response.meta['tid']
        item['replynums'] = response.meta['replynums']
        item['title'] = response.meta['title']
        item['page'] = response.meta['page']
        item['comments'] = comments.strip()
        return item










