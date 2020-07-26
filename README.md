## **项目名称**

基于微博评论的简单舆论分析 -- python设计

### **上手指南**

1. 建立mysql数据库，源码中账户与密码皆为root
2. 对**https://weibo.com**进行数据挖掘
3. 下载500w基础微博预料，[下载地址](https://pan.baidu.com/share/init?errmsg=Auth+Login+Sucess&errno=0&ssnerror=0&&surl=eSeXh5K) => 提取密码为: tvdo，并导入mysql数据库
4. 下载50w消极及50w积极.csv(已进行分类化)，下载链接：https://pan.baidu.com/s/1AOVB_kYkcbkDAEGjZ08v5Q  提取码：z5f0
5. 具体分析以及部署请看论文部分

**运行环境说明**

开发语言：Python 3.7.3 

开发环境：64位Windows10系统，12G运行内存，AMD 2500U处理器。 

数据库：MySQL5.56

开发工具:Python编辑器：PyCharm 2019.1；

MySQL管理工具：SQLyog12.9 

使用说明: 1）本机电脑要安装有MySQL，并且账号密码皆为root。若密码不是root，请在源代码改变MySQL中的账号与密码。2）本机内存需要大于8GB(最低要求为8G)，因为需要训练模型，将大容量数据装载进内存，若不过8GB，请不要训练模型，直接使用提供好的模型。3）在运行前，确保python版本>3.0，安装代码所需要的所有依赖库。执行```pip install -r requirements.txt```

**情感分析**

![情感分析](https://ae01.alicdn.com/kf/H519ce8f4b14a412a8473d1475b3214f97.png)

**中文情感分析建模**

使用mysql导入500w微博数据语料: ```mysql –u用户名 –p密码 <weibo500w.sql```

对微博语料进行情感分类，是基于原有SnowNLP进行积极和消极情感分类和训练。得到新的模型数据。基准为>0.8为积极评论，<0.3为消极评论，进行二分类。

训练完成后会生成```sentiment.marshal.3```模型文件，将python位置```/Lib/site-packages/snownlp/sentiment/中sentiment.marshal.3```直接替换，训练可以进行多轮训练，精度会更好(但是不建议，个人电脑内存小且运行速度慢)。使用模型的方法也很简单，直接将文本文件导入模型中，就会自动分析每句话的情感积极度。

###### **基于机器学习的方法**

使用jieba分词，对数据集的切分，以第一列评论数据作为特征，以第二列分数作为标签，按照8：2切分训练集和测试集。然后就用sklearn中自带的朴素贝叶斯算法训练，得到最后我们的机器学习模型。

**数据可视化(以广东第二师范学院微博为例)**

![数据展示](https://ae03.alicdn.com/kf/H566b1b8f21da4b45a0e12f670515a156d.png)

![1e51b1549b1d5bbfc9fbfaf873e2621.png](https://ae04.alicdn.com/kf/Hd8eca7c6601146a490e4e2a938866fbaI.png)

![6e35fe84e48e29ad0e2f8f3fae50ac3.png](https://ae02.alicdn.com/kf/H3e96253773814161865d42b42b9b8e8do.png)![8a57866235bd804db5acb2635feaa94.png](https://ae05.alicdn.com/kf/H91648a9e35544ef7b63978ad03481824C.png)

![33780f0d9597b63e040812563be6920.png](https://ae04.alicdn.com/kf/He6d588cd86b04d519d4b78bd2ed9c2b5S.png)

![899b9954675eebeb0ca675b52f48b92.png](https://ae03.alicdn.com/kf/He04b837f3ee3485db403d4f994092a25K.png)

![898422e6dc76d1589706b8809de85af.png](https://ae06.alicdn.com/kf/H53976cb6a1504ebb86e7af7785fd349bz.png)

![a10796c9fddaf82d6b340b1812daef6.png](https://ae01.alicdn.com/kf/Hb1b8c85a204c45cb932658dd3cf4f8adt.png)

![c7c4cf96751b17563a67b1cf7d7026a.png](https://ae01.alicdn.com/kf/Hb340d91b3b9a4a1084ab8cf811aa9cb8w.png)

![ea2357e61c840ba0158c877adfaf73c.png](https://ae01.alicdn.com/kf/H3f3cb9293f614deeaa42cd241e04912f6.png)

**小结**

实现了中文情感分析两种方法，其中建立的两个模型，通用性很强。只要将数据改成自己所要分析的数据，模型就能给予总体的分数。若换为淘宝京东等电商的购物评论，依旧可以使用第二章所用到的爬虫技术抓取相对应的数据，然后对数据使用这一章知识进行建模，得到专属于购物评论的模型。总体而言，效果基本达到预期。

###### 



