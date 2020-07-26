import json

import scrapy

from weibo.items import WeiboItem
from bs4 import BeautifulSoup


class weibo_spider(scrapy.Spider):
    name = "weibo"
    start_urls = [
        "https://m.weibo.cn/api/container/getIndex?uid=1905379401&luicode=10000011&lfid=100103type%3D1%26q%3D%E5%B9%BF%E4%B8%9C%E7%AC%AC%E4%BA%8C&sudaref=m.weibo.cn&display=0&retcode=6102&type=uid&value=1905379401&containerid=1076031905379401"]
    url = "https://m.weibo.cn/api/container/getIndex?uid=1905379401&luicode=10000011&lfid=100103type%3D1%26q%3D%E5%B9%BF%E4%B8%9C%E7%AC%AC%E4%BA%8C&sudaref=m.weibo.cn&display=0&retcode=6102&type=uid&value=1905379401&containerid=1076031905379401&since_id="
    # start_urls = ["https://m.weibo.cn/"]
    allowed_domains = ["weibo.com", "weibo.cn"]
    since_id = ""  # 下下面的id
    created_at = ""  # 创建的日期
    text = ""  # 发布的内容
    source = ""  # 发布文章的设备
    scheme = ""  # 原文连接
    reposts_count = 0  # 转发数量
    textLength = 0  # 文章字数
    comments_count = 0  # 评论个数
    attitudes_count = 0  # 点赞个数

    def parse(self, response):
        text_json = json.loads(response.body_as_unicode())
        self.since_id = text_json.get('data').get('cardlistInfo').get('since_id')
        cards = text_json.get('data').get('cards')
        for it in cards:
            it_son = it.get('mblog')
            if it_son:
                self.created_at = it_son['created_at']
                self.text = it_son['text']
                self.source = it_son['source']
                self.scheme = it['scheme']
                self.reposts_count = it_son['reposts_count']
                self.comments_count = it_son['comments_count']
                self.attitudes_count = it_son['attitudes_count']
                soup = BeautifulSoup(str(self.text), "html.parser")
                self.text = soup.get_text()
                if len(self.created_at) < 6:
                    self.created_at = "%s%s" % ("2020-", self.created_at)
                self.textLength = len(self.text)
                items = WeiboItem(created_at=self.created_at, text=self.text, source=self.source, scheme=self.scheme,
                                  reposts_count=self.reposts_count, comments_count=self.comments_count,
                                  attitudes_count=self.attitudes_count, textLength=self.textLength)
                yield items
        if not self.since_id:
            return
        urls = "%s%s" % (self.url, str(self.since_id))
        yield scrapy.Request(urls, callback=self.parse)
