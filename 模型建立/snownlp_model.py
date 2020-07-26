# encoding:utf-8

import re
import pymysql
from snownlp import SnowNLP
from snownlp import sentiment

conn = pymysql.connect(host='localhost', user='root', password='root', charset="utf8", use_unicode=False)  # 连接服务器
print("连接成功")
with conn:
    cur = conn.cursor()
    cur.execute("SELECT * FROM test.weibo WHERE weiboId < '%d'" % 6000000)
    rows = cur.fetchall()
comment = []
for row in rows:
    row = list(row)
    comment.append(row[18])

print("评论加载成功")

def train_model(texts):
    for li in texts:
        comm = li.decode('utf-8')
        text = re.sub(r'(?:回复)?(?://)?@[\w\u2E80-\u9FFF]+:?|\[\w+\]', ',', comm)
        socre = SnowNLP(text)
        if socre.sentiments > 0.8:
            with open('pos.txt', mode='a', encoding='utf-8') as g:
                g.writelines(comm + "\n")
        elif socre.sentiments < 0.3:
            with open('neg.txt', mode='a', encoding='utf-8') as f:
                f.writelines(comm + "\n")
        else:
            pass


train_model(comment)
print("500w结束")
sentiment.train('neg.txt', 'pos.txt')
print("开始保存")
sentiment.save('sentiment.marshal')
print("保存结束")