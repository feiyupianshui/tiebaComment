# import csv
# import pandas
import os
from wordcloud import WordCloud
import matplotlib.pyplot as plt
import re
import jieba
import jieba.analyse
from jieba.analyse import extract_tags
import jieba.posseg as pseg
from snownlp import SnowNLP
from scipy.misc import imread


# csvfile = open(r'C:\Users\D18\Desktop\posttest.csv', 'r', encoding='utf-8')
# Dictdata = csv.DictReader(csvfile)
# #把列表/字典拼成一个字符串的方式，之前还有一种方式是".join(list)，也挺好用
# title = ''
# for row in Dictdata:
#     title = title + row.get('标题')
# print(title)

# csvdata = pandas.read_csv(r'C:\Users\D18\Desktop\posttest.csv',header=0,encoding='utf-8')
# print(csvdata)
'''
打不开的话记得检查：
1、是不是只写了路径没写文件名；
2、文件的编码方式和指定打开的编码方式是不是不同；
3、文件名最好用英文，路径字符串最好是拼接好用变量传进去
'''
# txtObj = open(r'C:\Users\D18\Desktop\readtest.txt', 'r', encoding='utf-8')
# x = txtObj.read()
#以下能筛选掉大部分垃圾
# pattern = re.compile('[A-Za-z0-9_]+|\n+|[-_=+.,"?!“”～，；？。！、…—（）@#\\\\ ]+')
# result = re.sub(pattern,"", x)
#match和search都只能匹配第一个
# y = re.match('[^x00-xff]+', x)
# z = y.group(1)

# pattern = re.compile(r'[\u4e00-\u9fa5]+')
# filter_data = re.findall(pattern, x)
# cleaned_comments = "".join(filter_data)
# jieba.load_userdict(r'C:\Users\D18\Desktop\mydict.txt')#这个是把库分错了的修正
#
# stopwords = ['你', '了', '吗', '我', '的', '是']
# segs = jieba.lcut(cleaned_comments)
# seg = [s for s in segs if s not in stopwords]

# posseg1 = pseg.lcut(cleaned_comments)

# seg = jieba.analyse.extract_tags(cleaned_comments, topK=5, withWeight=False, allowPOS=())
# print(seg)

# s = SnowNLP(x)
# print(s.sentiments)

font = os.path.join(os.path.dirname(__file__), "c:\\windows\\fonts\\simhei.ttf")

# def cloud(data):
#     wc = WordCloud(font_path=font, background_color='#ff7f58') #词云实例化
#     wc.generate_from_frequencies(data) #根据频率生成词云图
#     plt.imshow(wc) #显示
#     plt.axis('off') #因为matplot是个二位的矩阵图，这里不适用，所以要关掉坐标显示
#     plt.show()#再显示
#
# cloud(data={"隔离":100, "种族":50, "主义":10})
def GeneratePicture(txtname, max_words, Picname,color):
	path = os.getcwd()
	if '\\' in path:
		txtfile = path + '\\' + txtname + '.txt'
	else:
		txtfile = path + '/' + txtname + '.txt'
	content = open(txtfile, 'r', encoding='utf-8').read()  #评论内容
	#根据tf-idf值找出文件中的关键词
	tags = extract_tags(content, topK=max_words)
	#分析得到关键词的词频
	word_freq_dict = dict()
	word_list = jieba.lcut(content)
	for tag in tags:
		freq = word_list.count(tag)
		word_freq_dict[tag] = freq
	#设置背景图片
	if Picname:
		if '\\' in path:
			background = path + '\\' + Picname
		else:
			background = path + '/' + Picname
		back_coloring = imread(background)
		wc = WordCloud(font_path=font,
			           background_color=color, #背景颜色
					   max_words= max_words,# 词云显示的最大词数
					   max_font_size=100, #字体最大值
					   mask = back_coloring) #背景图

	else:
		wc = WordCloud(font_path=font,
			           background_color=color,    # 背景颜色
					   max_words=max_words,       # 词云显示的最大词数
					   max_font_size=100)         # 字体最大值

	wc.generate_from_frequencies(word_freq_dict)
	plt.imshow(wc)
	plt.axis("off")
	plt.show()  # 绘制词云
	#保存图片
	if '\\' in path:
		pic_file = path + '\\' + txtname + '%d.png' % max_words
	else:
		pic_file = path + '/' + txtname + '%d.png' % max_words
	wc.to_file(pic_file)


GeneratePicture(txtname = 'cleanedcomments', max_words=50, Picname='timg.png',color = '#00314F')
