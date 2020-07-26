import datetime

import pymysql

account = {
    'user': 'root',
    'password': 'root',
    'host': 'localhost',
    'database': 'test'
}


def mysqlConnect(account):
    connect = pymysql.connect(**account)
    return connect


def getMessage(cursor, month, day, year, publish_tool, up_num, retweet_num, comment_num, textLength, publish_time):
    sql = 'select * from data_copy ORDER BY publish_time'
    cursor.execute(sql)
    row = cursor.fetchall()
    Day = {}  # 建立字典便于统计每天发送的微博
    Year = {}
    Month = {}
    for i in range(1, 32):
        Day[i] = 0
    for i in range(1, 13):
        Month[i] = 0
    for i in range(2016, 2021):
        Year[i] = 0

    for it in row:
        date = datetime.datetime.strptime(it['publish_time'], "%Y-%m-%d %H:%M:%S")
        print(date.year)
        Year[date.year] += 1
        Day[date.day] += 1
        Month[date.month] += 1
        publish_tool.append(it['publish_tool'])
        comment_num.append(it['up_num'])
        retweet_num.append(it['retweet_num'])
        comment_num.append(it['comment_num'])
        textLength.append(it['textLength'])
        publish_time.append(it['publish_time'])

    for i in range(1, 32):
        day.append(Day[i])
    for i in range(1, 13):
        month.append(Month[i])
    for i in range(2016, 2021):
        year.append(Year[i])


if __name__ == '__main__':
    month = []  # 按照月发送的微博
    year = []  # 按照年发送的微博
    day = []  # 按照日发送的微博
    publish_tool = []  # 手机的种类
    up_num = []  # 点赞数
    retweet_num = []  # 转发数
    comment_num = []  # 评论数
    textLength = []  # 发送微博长度
    publish_time = []  # 时间
    connect = mysqlConnect(account)
    cursor = connect.cursor(cursor=pymysql.cursors.DictCursor)
    getMessage(cursor, month, day, year, publish_tool, up_num, retweet_num, comment_num, textLength, publish_time)
    # 数据可视化

    from pyecharts.charts import Bar
    from pyecharts import options as opts

    # 按照日 发微博的个数
    xday = []
    for i in range(1, 32):
        xday.append(i)
    bar = (
        Bar()
            .add_xaxis(xday)
            .add_yaxis("每天发送的微博", day)
            .set_global_opts(title_opts=opts.TitleOpts(title="人民日报发微博统计"))
    )
    bar.render(path='day.html')
    # 按月
    xmonth = []
    for i in range(1, 13):
        xmonth.append(i)
    bar = (
        Bar()
            .add_xaxis(xmonth)
            .add_yaxis("每月发送的微博", month)
            .set_global_opts(title_opts=opts.TitleOpts(title="人民日报发微博统计"))
    )
    bar.render(path='month.html')
    # 按年
    xyear = []
    for i in range(2016, 2021):
        xyear.append(i)
    bar = (
        Bar()
            .add_xaxis(xyear)
            .add_yaxis("每年发送的微博", year)
            .set_global_opts(title_opts=opts.TitleOpts(title="人民日报发微博统计"))
    )
    bar.render(path='year.html')

    # 分析手机
    Phone = {}
    for it in publish_tool:
        Phone[it] = 0
    for it in publish_tool:
        Phone[it] += 1

    from pyecharts import options as opts
    from pyecharts.charts import Pie

    c = (
        Pie()
            .add("", [list(z) for z in zip(Phone.keys(), Phone.values())])
            .set_colors(["blue", "green", "yellow", "red", "pink", "orange", "purple"])
            .set_global_opts(title_opts=opts.TitleOpts(title="人民日报发微博的设备"))
            .set_series_opts(label_opts=opts.LabelOpts(formatter="{b}: {c}"))
            .render("phone.html")
    )

    # 分析按时间 点赞 评论 转发

    import pyecharts.options as opts
    from pyecharts.charts import Line

    c = (
        Line()
            .add_xaxis(publish_time)
            .add_yaxis("点赞", up_num, is_smooth=True)
            .add_yaxis("转发", retweet_num, is_smooth=True)
            .add_yaxis("评论", comment_num, is_smooth=True)
            .add_yaxis("文章长度", textLength, is_smooth=True)
            .set_global_opts(title_opts=opts.TitleOpts(title="人民日报微博转发点赞等数据"))
            .render("msg.html")
    )
