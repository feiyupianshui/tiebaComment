#!/use/bin/env python
#_*_coding:utf-8_*_
import requests
import re


baseUrl = r'https://tieba.baidu.com/f?kw=%E6%88%92%E8%B5%8C&ie=utf-8&pn={pn}'
headers = {"User-Agent": "Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.100 Safari/537.36"}
cookies = {"Cookie": "BAIDUID=A6E139B54571CC652E26FF2ACF555BBE:FG=1; PSTM=1506316275; BIDUPSID=861EC6D180D7AEC1370D8DEA07FC639E; TIEBA_USERTYPE=11a9867d81a3687b4246720f; bdshare_firstime=1506582548004; __cfduid=d1a93acf1fbb522eb47d394990f43ff9b1508725303; MCITY=-179%3A75%3A; fixed_bar=1; bottleBubble=1; FP_LASTTIME=1509932977010; FP_UID=0d8ea68b1941be419e7685f3e908b0f7; TIEBAUID=18658700369be7572fd8169c; baidu_broswer_setup_%E6%B2%99%E6%BC%A0%E4%B8%80%E9%81%93%E9%A3%8E%E6%99%AF%E7%BA%BF=0; PSINO=3; H_PS_PSSID=1425_21106_24879_22073; BDORZ=B490B5EBF6F3CD402E515D22BCDA1598; wise_device=0"}


# 清洗评论
class Tool:
    #去除img标签,7位长空格
    removeImg = re.compile('<img.*?>| {7}|')
    #删除超链接标签
    removeAddr = re.compile('<a.*?>|</a>')
    #把换行的标签换为\n
    replaceLine = re.compile('<tr>|<div>|</div>|</p>')
    #将表格制表<td>替换为\t
    replaceTD= re.compile('<td>')
    #把段落开头换为\n加空两格
    replacePara = re.compile('<p.*?>')
    #将换行符或双换行符替换为\n
    replaceBR = re.compile('<br><br>|<br>')
    #将其余标签剔除
    removeExtraTag = re.compile('<.*?>')
    def replace(self,x):
        x = re.sub(self.removeImg, "", x)
        x = re.sub(self.removeAddr, "", x)
        x = re.sub(self.replaceLine, "\n", x)
        x = re.sub(self.replaceTD, "\t", x)
        x = re.sub(self.replacePara, "\n    ", x)
        x = re.sub(self.replaceBR, "\n", x)
        x = re.sub(self.removeExtraTag, "", x)
        #strip()将前后多余内容删除
        return x.strip()

class BDTB:
    def __init__(self, baseUrl, floorTag):
        self.tool = Tool()
        self.baseUrl = baseUrl
        # 全局file变量，文件写入操作对象
        self.file = None
        # 楼层标号，初始为1
        self.floor = 1
        # 默认的标题，如果没有成功获取到标题的话则会用这个标题
        self.defaultTitle = u"百度贴吧"
        # 是否写入楼分隔符的标记
        self.floorTag = floorTag


    # 抓取x->y页的所有帖子的评论和回复文字
    def startCrawl(self, startpage, endpage):
        #获取总链接列表并打印出来
        totalurls = []
        for i in range(startpage-1, endpage):
            print('收集第'+str(startpage)+'页至第'+str(endpage)+'页帖子链接')
            for ut in self.getUrlTails(i):
                totalurls.append(ut)

        #以下只是打印数据，无逻辑关系
        urls_num = str(len(totalurls))
        print('共收集到' + urls_num + '条帖子')
        for url in totalurls:
            print('所有帖子链接列表为：')
            print(url)

        #访问每个具体帖子
        for x in totalurls:
            print('访问贴id：'+ str(x[3:]))
            detail_urls = self.getDetailUrls(x)
            print('该贴共'+ str(len(detail_urls))+'页')
            if len(detail_urls) != 0:
                for item in detail_urls:
                    respon = requests.get(item, headers=headers, cookies=cookies)
                    title = self.getTitle(respon)
                    self.setFileTitle(title)
                    comments = self.getComments(respon)
                    # replys = self.getReplys(respon)
                    self.writeData(comments)
                    # self.writeData(replys)
            else:
                print('URL已失效，页面不存在')


    # 获取第X页的所有帖子的链接, return list
    def getUrlTails(self, pagenum):
        main_url = self.baseUrl.format(pn=pagenum * 50)
        resp = requests.get(main_url, headers=headers, cookies=cookies)
        pattern = re.compile('<a href="(.*?)".*?class="j_th_tit ">.*?</a>')
        url_tails = re.findall(pattern, resp.text)
        return url_tails

    # 获取某个帖子的标题, return str
    def getTitle(self, respon):
        pattern6 = re.compile('<h3 class="core_title_txt pull-left text-overflow  ".*?>(.*?)</h3>')
        title = re.search(pattern6, respon.text)
        if title:
            return title.group(1).strip()
        else:
            return None

    # 获取某个帖子的总回复数, return int
    def getReplyNum(self, respon):
        pattern3 = re.compile('<span class="red".*?>(.*?)</span>')
        reply_num = re.search(pattern3, respon.text)
        return int(reply_num.group(1))

    # 获取某贴总页数, return int
    def getPageNum(self, respon):
        pattern2 = re.compile('<span class="red">(.*?)</span>')
        page_num = re.search(pattern2, respon.text)
        return int(page_num.group(1))

    # 获取某个帖子的所有页面的链接, return list
    def getDetailUrls(self, url_tail):
        detailurls = []
        URL = 'https://tieba.baidu.com'
        first_url = URL + url_tail +'?pn={1}'#其实可以不加后面的页面参数，但是为了和后面的链接列表保持一致，这样访问的时候可以直接取缓存内容
        first_resp = requests.get(first_url, headers=headers, cookies=cookies)
        page_num = self.getPageNum(first_resp)
        if page_num == None:
            print("URL已失效，请重试")
            return
        else:
            for x in range(1, page_num+1):
                detailurls.append(URL + url_tail + '?pn={' + str(x) + '}')
            return detailurls

    # 获取帖子某页的所有楼层内容,return list
    def getComments(self, respon):
        pattern4 = re.compile('<div>.*?class="d_post_content j_d_post_content ">(.*?)</div>')
        items = re.findall(pattern4, respon.text)
        comments = []
        for item in items:
            comment = "\n" + self.tool.replace(item) + "\n"
            comments.append(comment.encode('utf-8'))
        return comments #list

    # 获取帖子某页所有楼层回复，失败
    def getReplys(self, respon):
        pattern5 = re.compile('<span class="lzl_content_main">(.*?)</span>')
        replys = re.findall(pattern5, respon.text)
        return replys #list

    #存入标题
    def setFileTitle(self, title):
        # 如果标题不是为None，即成功获取到标题
        if title is not None:
            self.file = open(title + ".txt", "w+")
        else:
            self.file = open(self.defaultTitle + ".txt", "w+")

    #把评论写入文件
    def writeData(self, comments):
        # 向文件写入每一楼的信息
        for m in comments:
            if self.floorTag == '1':
                # 楼之间的分隔符
                floorLine = "\n" + str(
                    self.floor) + u"-----------------------------------------------------------------------------------------\n"
                self.file.write(floorLine)
            self.file.write(m)
            self.floor += 1

