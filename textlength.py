import re

data = open("C:\\Users\\D18\\Desktop\\contragambling\\nogamblingcomments.txt", 'r', encoding='utf-8')
x = data.read()
pattern = re.compile('[A-Za-z0-9_]+|\n+|[-_=+.,"?!“”～，；？。！、…—（）@#\\\\ ]+')
result = re.sub(pattern, "", x)
words = [x for x in jieba.cut(result) if len(x) >= 2]
c = Counter(words).most_common(20)
with open('TFrequency.csv', 'w+', encoding='utf-8') as csvfile:
    writer = csv.writer(csvfile)
    writer.writerows(c)
print(c, end=' ')