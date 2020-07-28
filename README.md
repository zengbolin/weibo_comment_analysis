## **项目名称**

基于微博评论的简单舆论分析 -- python设计

### **上手指南**

1. 建立mysql数据库，源码中账户与密码皆为root
2. 对 **https://weibo.com** 进行数据挖掘
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

[![aEIVRx.jpg](https://s1.ax1x.com/2020/07/28/aEIVRx.jpg)](https://imgchr.com/i/aEIVRx)

**中文情感分析建模**

使用mysql导入500w微博数据语料: ```mysql –u用户名 –p密码 <weibo500w.sql```

对微博语料进行情感分类，是基于原有SnowNLP进行积极和消极情感分类和训练。得到新的模型数据。基准为>0.8为积极评论，<0.3为消极评论，进行二分类。

训练完成后会生成```sentiment.marshal.3```模型文件，将python位置```/Lib/site-packages/snownlp/sentiment/中sentiment.marshal.3```直接替换，训练可以进行多轮训练，精度会更好(但是不建议，个人电脑内存小且运行速度慢)。使用模型的方法也很简单，直接将文本文件导入模型中，就会自动分析每句话的情感积极度。

###### **基于机器学习的方法**

使用jieba分词，对数据集的切分，以第一列评论数据作为特征，以第二列分数作为标签，按照8：2切分训练集和测试集。然后就用sklearn中自带的朴素贝叶斯算法训练，得到最后我们的机器学习模型。

**数据可视化(以广东第二师范学院微博为例)**

![aE52ad.png](https://s1.ax1x.com/2020/07/28/aE52ad.png)

![aE5DxK.png](https://s1.ax1x.com/2020/07/28/aE5DxK.png)

![aE5sKO.png](https://s1.ax1x.com/2020/07/28/aE5sKO.png)

![aE5B26.png](https://s1.ax1x.com/2020/07/28/aE5B26.png)

![aE5gVH.png](https://s1.ax1x.com/2020/07/28/aE5gVH.png)

![aE5yrD.png](https://s1.ax1x.com/2020/07/28/aE5yrD.png)

![aE56qe.png](https://s1.ax1x.com/2020/07/28/aE56qe.png)

![aE5RIA.png](https://s1.ax1x.com/2020/07/28/aE5RIA.png)

![aE54RP.png](https://s1.ax1x.com/2020/07/28/aE54RP.png)

![aE5fPI.png](https://s1.ax1x.com/2020/07/28/aE5fPI.png)

**小结**

实现了中文情感分析两种方法，其中建立的两个模型，通用性很强。只要将数据改成自己所要分析的数据，模型就能给予总体的分数。若换为淘宝京东等电商的购物评论，依旧可以使用第二章所用到的爬虫技术抓取相对应的数据，然后对数据使用这一章知识进行建模，得到专属于购物评论的模型。总体而言，效果基本达到预期。
