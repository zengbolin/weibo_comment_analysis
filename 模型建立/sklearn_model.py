# encoding:utf-8
import jieba
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.naive_bayes import MultinomialNB


# 将中文分词
def chinese_word_cut(mytext):
    return " ".join(jieba.cut(mytext))


# 获得csv中的数据，并切分数据集
def get_data(file_path):
    data = pd.read_csv(file_path, encoding="utf-8")

    data['cut_comment'] = data.comment.apply(chinese_word_cut)
    X = data['cut_comment']
    y = data.score
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=22)

    return X_train, X_test, y_train, y_test


# 获得停词表中的虚词等
def get_custom_stopwords(stop_words_file):
    with open(stop_words_file, 'r', encoding="utf-8") as f:
        stopwords = f.read()
    stopwords_list = stopwords.split('\n')
    custom_stopwords_list = [i for i in stopwords_list]
    return custom_stopwords_list


# 训练模型，得到模型
def train(stoped_txt):
    stop_words_file = stoped_txt
    stopwords = get_custom_stopwords(stop_words_file)

    vect = CountVectorizer(max_df=0.8,
                           min_df=3,
                           token_pattern=u'(?u)\\b[^\\d\\W]\\w+\\b',
                           stop_words=frozenset(stopwords))

    model = MultinomialNB()

    return vect, model


if __name__ == '__main__':
    # 若文本数据以及停词表数据不一样，可以直接修改文本位置
    X_train, X_test, y_train, y_test = get_data(r'50w消极及50w积极.csv')
    vect, model = train(r'stoped.txt')

    X_train_vect = vect.fit_transform(X_train)  # 将训练集塞进vect中
    model.fit(X_train_vect, y_train)  # 拟合模型
    train_score = model.score(X_train_vect, y_train)  # 求模型在训练集的分数
    print("训练集得到的分数:", train_score * 100)

    X_test_vect = vect.transform(X_test)
    print("测试集得到的分数:", model.score(X_test_vect, y_test) * 100)  # 求模型在测试集的分数
