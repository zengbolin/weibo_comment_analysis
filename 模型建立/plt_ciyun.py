# encoding:utf-8
from os import path
import jieba
import matplotlib.pyplot as plt
from wordcloud import WordCloud, STOPWORDS, ImageColorGenerator


def WorldCloud_pic(text_path, pic_path, font_path):
    text = open(text_path, 'r', encoding='UTF-8').read()
    word_list = jieba.cut(text, cut_all=False)
    wl_space_split = " ".join(word_list)
    print(wl_space_split)
    backgroud_Image = plt.imread(pic_path)
    print('加载图片成功！')
    stopwords = STOPWORDS.copy() # 使用词云自带的停词表
    stopwords.add("哈哈")  # 可以加多个屏蔽词
    wc = WordCloud(
        width=1024,
        height=768,
        background_color='white',  # 设置背景颜色
        mask=backgroud_Image,  # 设置背景图片
        font_path=font_path,  # 设置中文字体，若是有中文的话，这句代码必须添加，不然会出现方框，不出现汉字
        max_words=600,  # 设置最大现实的字数
        stopwords=stopwords,  # 设置停用词
        max_font_size=400,  # 设置字体最大值
        random_state=50,  # 设置有多少种随机生成状态，即有多少种配色方案
    )
    wc.generate_from_text(wl_space_split)  # 开始加载文本
    img_colors = ImageColorGenerator(backgroud_Image)
    wc.recolor(color_func=img_colors)  # 字体颜色为背景图片的颜色
    plt.imshow(wc)  # 显示词云图
    plt.axis('off')  # 是否显示x轴、y轴下标
    plt.show()  # 显示
    d = path.dirname(__file__) # 获得模块所在的路径的
    wc.to_file(path.join(d, "词云.jpg"))
    print('生成词云成功!')


if __name__ == '__main__':
    text_path = input("请输入文本位置:")
    pic_path = input("请输入背景图的位置:")
    font_path = input("请输入中文字体的位置(会乱码):")
    WorldCloud_pic(text_path, pic_path, font_path)
