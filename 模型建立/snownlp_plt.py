# encoding:utf-8
import numpy as np
from snownlp import SnowNLP
import matplotlib.pyplot as plt
import re


def get_comment(path):
    comment = []
    with open("评论.txt", mode='w', encoding='utf-8') as file:
        file.write(" ")
    with open(path, mode='r', encoding='utf-8') as f:
        rows = f.readlines()
        # print(rows)
        for row in rows:
            if row not in comment:
                comments = re.search('"comment_info": "：(.*?)"', row, re.S).group(1).replace(r"\xa0", "")
                with open("评论.txt", mode='a+', encoding='utf-8') as file:
                    file.write(comments)
                    file.write("\n")
                comment.append(comments)
    return comment


def snowan_alysis(comment):
    sentimentslist = []
    for li in comment:
        if li == "":
            pass
        else:
            print(li)
            s = SnowNLP(li)
            print(s.sentiments)
            sentimentslist.append(s.sentiments)
    plt.hist(sentimentslist, bins=np.arange(0, 1, 0.01))
    plt.show()


if __name__ == '__main__':
    text_path = input("请输入文本文件的位置:")
    snowan_alysis(get_comment(text_path))
