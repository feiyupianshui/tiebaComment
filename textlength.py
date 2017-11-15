import re

data = open("C:\\Users\\D18\\Desktop\\contragambling\\nogamblingcomments.txt", 'r', encoding='utf-8')
x = data.read()
pattern = re.compile('[A-Za-z0-9_]+|\n+|[-_=+.,"?!“”～，；？。！、…—（）@#\\\\ ]+')
result = re.sub(pattern, "", x)
print(len(x))