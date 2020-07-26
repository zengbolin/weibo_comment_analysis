# -*- coding: utf-8 -*-

import pymysql
import json


class WeiboPipeline(object):
    account = {
        'user': 'root',
        'password': 'root',
        'host': 'localhost',
        'database': 'python'
    }

    def mysqlConnect(self):
        connect = pymysql.connect(**self.account)
        return connect

    def __init__(self):
        self.connect = self.mysqlConnect()  # 连接数据库
        self. cursor = self.connect.cursor(cursor = pymysql.cursors.DictCursor)
        #### 以json写入
        #self.fp = open("xiaofuren.json", 'w', encoding='utf-8')

    def insertMsg(self, scheme, text, source, reposts_count, comments_count, attitudes_count, textLength, created_at):
        try:
            self.cursor.execute(
                "INSERT INTO %s VALUES( \'%s\' ,\' %s\' ,\' %s\',\' %d\',\' %d\',\' %d\',\' %d\',\' %s\')" % (
                    "weibo", scheme, text, source, reposts_count, comments_count, attitudes_count, textLength, created_at)
                )
            self.connect.commit()
        except Exception as e:
            print("insert_sql error: " + e)

    def open_spider(self, spider):
        print("爬虫开始了******************")

    def process_item(self, item, spider):
        self.insertMsg( item['scheme'], item['text'], item['source'], item['reposts_count'], item['comments_count'], item['attitudes_count'], item['textLength'], item['created_at'])
        return item
        #### 以json写入
        # itme_json = json.dumps(dict(item), ensure_ascii=False)
        # self.fp.write(itme_json + '\n')
        # return item

    def close_spider(self, spider):
        print("爬虫结束***************")
        print("数据写入成功")
        self.cursor.close()
