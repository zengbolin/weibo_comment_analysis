# -*- coding: utf-8 -*-
import scrapy


class WeiboItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    since_id = scrapy.Field()  # 下下面的id
    created_at = scrapy.Field()  # 创建的日期
    text = scrapy.Field()  # 发布的内容
    source = scrapy.Field()  # 发布文章的设备
    scheme = scrapy.Field()  # 原文连接
    reposts_count = scrapy.Field()  # 转发数量
    textLength = scrapy.Field()  # 文章字数
    comments_count = scrapy.Field()  # 评论个数
    attitudes_count = scrapy.Field()  # 点赞个数
