import codecs

import jieba.analyse
import pandas as pd

stopwords = [line.strip() for line in codecs.open('stoped.txt', 'r', 'utf-8').readlines()]

# 载入停用词
jieba.analyse.set_stop_words('stoped.txt')
segments = []

with open('澎湃新闻_第8条微博相关评论.txt', 'r', encoding="utf-8") as f:
    rows = f.readlines()
    for row in rows:
        # TextRank 关键词抽取，只获取固定词性
        # words = jieba.cut(row)
        words = jieba.analyse.textrank(row, topK=50,withWeight=False,allowPOS=('ns', 'n', 'vn', 'v','r','v'))
        splitedStr = ''
        for word in words:
            # 停用词判断，如果当前的关键词不在停用词库中才进行记录
            if word not in stopwords:
                # 记录全局分词
                segments.append({'word': word, 'count': 1})
                splitedStr += word + ' '

# 将结果数组转为df序列
dfSg = pd.DataFrame(segments)

# 词频统计
dfWord = dfSg.groupby('word')['count'].sum()
print(dfWord)