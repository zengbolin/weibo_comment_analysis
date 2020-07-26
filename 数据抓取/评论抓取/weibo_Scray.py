# -*- coding: utf-8 -*-

import requests
import json
import time
from lxml import etree
import re


class Weibospider:
    # 初始化函数
    def __init__(self, uid, count, name):
        # 获取首页的相关信息：
        self.uid = uid  # 微博特有id
        self.name = name  # 传入微博用户名
        self.start_url = 'https://weibo.com/u/' + self.uid + '?page={}&is_all=1'  # 微博个人主页地址
        self.count = count  # 定义爬取的页数
        # 定义伪装浏览器参数
        self.headers = {
            "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8",
            "accept-encoding": "gzip, deflate, br",
            "accept-language": "zh-CN,zh;q=0.9,en;q=0.8",
            "cache-control": "max-age=0",
            "cookie": "UOR=,,www.baidu.com; SINAGLOBAL=865021701701.2163.1569236889711; _s_tentry=www.baidu.com; Apache=8733171935959.907.1590556807448; ULV=1590556807473:25:1:1:8733171935959.907.1590556807448:1582275304836; login_sid_t=9e20f0d2ce967d9968cbc289eafaf498; cross_origin_proto=SSL; SUBP=0033WrSXqPxfM725Ws9jqgMF55529P9D9WFufpeXJopR9v4xBMTE4w535JpX5K2hUgL.Foqfeh.0Sh.EeKn2dJLoIEBLxKqL1hqLBKMLxKqL1hqLB-eLxKMLBK.LB.2LxKML1hBLBK2t; ALF=1622093723; SSOLoginState=1590557723; SCF=Ag49MyVuR122G3i0uhEOR1ZaqV4TkUPn2D5UEdh43M_gvcJN8QnjAYoPP4122nihFaycmePDsJgzHa5esU9qe7I.; SUB=_2A25zyYxMDeRhGeBL61sS9CfOyjSIHXVQvvqErDV8PUNbmtAKLW_tkW9NR0U2nxa0_G2u_QgzkMEYaf1lpmhIzBL5; SUHB=0k1CrgQ48C58HP; un=13269880512; wvr=6; WBStorage=42212210b087ca50|undefined; webim_unReadCount=%7B%22time%22%3A1590560269861%2C%22dm_pub_total%22%3A0%2C%22chat_group_client%22%3A0%2C%22chat_group_notice%22%3A0%2C%22allcountNum%22%3A16%2C%22msgbox%22%3A0%7D",
            "referer": "https://www.weibo.com/u/" + self.uid + "?topnav=1&wvr=6&topsug=1",
            "upgrade-insecure-requests": "1",
            "user-agent": "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/72.0.3626.96 Safari/537.36",
        }
        # 定义几个代理
        self.proxy = {
            'HTTP': 'HTTP://180.125.70.78:9999',
            'HTTP': 'HTTP://117.90.4.230:9999',
            'HTTP': 'HTTP://111.77.196.229:9999',
            'HTTP': 'HTTP://111.177.183.57:9999',
            'HTTP': 'HTTP://123.55.98.146:9999',
            'HTTP': 'HTTP://106.14.47.5:80',
            'HTTP': 'HTTP://61.135.217.7:80',
            'HTTP': 'HTTP://58.53.128.83:3128',
            'HTTP': 'HTTP://58.118.228.7:1080',
            'HTTP': 'HTTP://221.212.117.10:808',
            'HTTP': 'HTTP://115.159.116.98:8118',
            'HTTP': 'HTTP://121.33.220.158:808',
            'HTTP': 'HTTP://124.243.226.18:8888',
            'HTTP': 'HTTP://124.235.135.87:80',
            'HTTP': 'HTTP://14.118.135.10:808',
            'HTTP': 'HTTP://119.176.51.135:53281',
            'HTTP': 'HTTP://114.94.10.232:43376',
            'HTTP': 'HTTP://218.79.86.236:54166',
            'HTTP': 'HTTP://221.224.136.211:35101',
            'HTTP': 'HTTP://58.56.149.198:53281'
        }

    def get_domain(self):
        text_1 = requests.get("https://s.weibo.com/weibo/{}".format(self.name), headers=self.headers).text
        html = "https://" + re.search('<a href="//(.*?)" target="_blank"', text_1, re.S).group(1).replace("//",
                                                                                                          "") + "?is_all=1"
        text_2 = requests.get(html, headers=self.headers).text
        domain = re.search("from=page_(.*?)&mod", text_2, re.S).group(1)

        return domain

    def parse_home_url(self, url):  # 处理解析首页面的详细信息（不包括两个通过ajax获取到的页面）
        res = requests.get(url, headers=self.headers)  # 获取首页的response
        response = res.text.replace("\\", "")  # 获取文本信息
        every_id = re.compile('name=(\d+)', re.S).findall(response)  # 利用正则表达式获取次级页面需要的id
        home_url = []  # 获取首页中微博的地址
        for id in every_id:
            base_url = 'https://weibo.com/aj/v6/comment/big?ajwvr=6&id={}&from=singleWeiBo'
            url = base_url.format(id)
            home_url.append(url)
        return home_url

    def parse_comment_info(self, url):  # 爬取直接发表评论的人的相关信息(name,info,time,info_url)
        res = requests.get(url, headers=self.headers)  # 请求网页
        response = res.json()  # 获取json数据
        count = response['data']['count']  # 获取微博评论的数量
        html = etree.HTML(response['data']['html'])  # 解析html数据(json中使用html存储评论数据)
        # 利用xpath分别分级获取各个节点的各个值
        name = html.xpath("//div[@class='list_li S_line1 clearfix']/div[@class='WB_face W_fl']/a/img/@alt")  # 评论人的姓名
        info = html.xpath("//div[@node-type='replywrap']/div[@class='WB_text']/text()")  # 评论信息
        info = "".join(info).replace(" ", "").split("\n")  # 将评论信息存储到info中，并去掉多余的换行符
        info.pop(0)  # 去掉第一个自己加进来的空格符号
        comment_time = html.xpath("//div[@class='WB_from S_txt2']/text()")  # 评论时间
        name_url = html.xpath("//div[@class='WB_face W_fl']/a/@href")  # 评论人的url
        name_url = ["https:" + i for i in name_url]  # 构建用户的地址
        comment_info_list = []  # 评论列表
        # 让每个item存储一条微博评论数据
        for i in range(len(name)):
            item = {}
            item["name"] = name[i]  # 存储评论人的网名
            item["comment_info"] = info[i]  # 存储评论的信息
            item["comment_time"] = comment_time[i]  # 存储评论时间
            item["comment_url"] = name_url[i]  # 存储评论人的相关主页
            comment_info_list.append(item)

        return count, comment_info_list

    def write_file(self, path_name, content_list):
        for content in content_list:
            with open(path_name, "a", encoding="UTF-8") as f:
                f.write(json.dumps(content, ensure_ascii=False))
                f.write("\n")

    def run(self):
        # 定义首页的爬取地址还有Ajax页面加载的网址
        start_url = self.start_url
        start_ajax_url_1 = 'https://weibo.com/p/aj/v6/mblog/mbloglist?ajwvr=6&domain=' + self.get_domain() + '&is_all=1&page={0}&pagebar=0&pl_name=Pl_Official_MyProfileFeed__20&id=' + self.get_domain() + self.uid + '&script_uri=/u/' + self.uid + '&pre_page={0}'
        start_ajax_url_2 = 'https://weibo.com/p/aj/v6/mblog/mbloglist?ajwvr=6&domain=' + self.get_domain() + '&is_all=1&page={0}&pagebar=1&pl_name=Pl_Official_MyProfileFeed__20&id=' + self.get_domain() + self.uid + '&script_uri=/u/' + self.uid + '&pre_page={0}'
        for i in range(self.count):  # 微博页数
            home_url = self.parse_home_url(start_url.format(i + 1))  # 获取每一页的微博
            ajax_url_1 = self.parse_home_url(start_ajax_url_1.format(i + 1))  # ajax加载页面的微博
            ajax_url_2 = self.parse_home_url(start_ajax_url_2.format(i + 1))  # ajax第二页加载页面的微博
            all_url = home_url + ajax_url_1 + ajax_url_2  # 获取其真正的url
            # 有多条评论就循环多少次
            for j in range(len(all_url)):
                print(all_url[j])
                path_name = self.name + "_第{}条微博相关评论.txt".format(i * 45 + j + 1)  # 生成文本的地址
                all_count, comment_info_list = self.parse_comment_info(all_url[j])  # 获取数目和评论数据
                self.write_file(path_name, comment_info_list)  # 写入文件
                # 设定最大阈值为1000000，因为一页15条评论，15*100w可达1500w
                for num in range(1, 1000000):
                    # 判断是否能继续爬取，一页15条数据
                    if num * 15 < int(all_count) + 15:
                        comment_url = all_url[j] + "&page={}".format(num + 1)  # 构成网址，加入page必要条件
                        print(comment_url)
                        try:
                            # 爬取评论并存储到文本
                            count, comment_info_list = self.parse_comment_info(comment_url)
                            self.write_file(path_name, comment_info_list)
                        except Exception as e:  # 发生错误，例如网络问题等，sleep一分钟继续爬
                            print("Error:", e)
                            time.sleep(60)
                            count, comment_info_list = self.parse_comment_info(comment_url)
                            self.write_file(path_name, comment_info_list)
                        finally:
                            del count
                            time.sleep(1)  # 删除count变量重新生成，并爬取每页停止一秒

                print("第{}微博信息获取完成！".format(i * 45 + j + 1))


# 获取微博用户的特有id
def get_uid(name):
    # 定义浏览器头部信息
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.87 Safari/537.36'}

    # 获取主页信息
    response = requests.get(f"https://s.weibo.com/weibo/{name}", headers=headers)
    # 将源代码转为文本信息
    html = response.text
    # 使用正则表达式处理得到的文本信息，提取uid
    uid = re.search("uid=(.*?) action", html, re.S).group(1)
    print(uid)
    return uid


# 主函数入口
if __name__ == '__main__':
    # 输入相对应的信息，包括用户名和爬取爬取微博的页数
    # 注意这里的页数不能超出原博的页数，且尽量少，毕竟微博大咖的一条微博评论数多达十几二十万，几页的话就很多了
    name = input("请输入你要爬取的微博名:")
    count = int(input("你要爬取用户微博的页数："))
    # 初始化类并执行
    weibo = Weibospider(uid=get_uid(name), count=count, name=name)
    weibo.run()
