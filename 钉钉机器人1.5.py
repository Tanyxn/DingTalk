# -*- coding:utf-8 -*-
# @Author : Tany
# @Date :2020-5-15

from gevent import monkey

monkey.patch_all()

from bs4 import BeautifulSoup
import gevent
from gevent.queue import Queue
import random
import requests
import json
import time

password = input('请输入启动密码：')
while password != 'kkb2020':
    password = input('密码错误，请重新输入输入启动密码或直接关闭退出：')


def sendmessage_start(access_token):
    """
    定义艾特所有人
    :param access_token:
    :param message:
    :return:
    """

    url = 'https://oapi.dingtalk.com/robot/send?access_token=%s' % access_token  # 钉钉机器人的webhook地址
    HEADERS = {
        "Content-Type": "application/json ;charset=utf-8 "
    }
    message = """
        今日知识点分享来啦
    """
    String_textMsg = {
        "msgtype": "text",
        "text": {"content": message},
        "at": {
            "atMobiles": [
                ""  # 如果需要@某人，这里写他的手机号
            ],
            "isAtAll": 1  # 如果需要@所有人，这些写1
        }
    }
    String_textMsg = json.dumps(String_textMsg)
    res = requests.post(url, data=String_textMsg, headers=HEADERS)
    print(res.text)


def sendmessage_content(access_token, message):
    """
    发送内容
    :param access_token:
    :param message:
    :return:
    """
    url = 'https://oapi.dingtalk.com/robot/send?access_token=%s' % (access_token)
    HEADERS = {
        "Content-Type": "application/json ;charset=utf-8 "
    }
    message = message
    String_textMsg = {
        "msgtype": "text",
        "text": {"content": message},
        "at": {
            "atMobiles": [
                ""  # 如果需要@某人，这里写他的手机号
            ],
            "isAtAll": 0  # 如果需要@所有人，这些写1
        }
    }
    String_textMsg = json.dumps(String_textMsg)
    res = requests.post(url, data=String_textMsg, headers=HEADERS)
    print(res.text)


def sendmessage_link(access_token, message):
    """
    实现发送链接
    :param access_token:
    :param message:
    :return:
    """
    url = 'https://oapi.dingtalk.com/robot/send?access_token=%s' % (access_token)
    HEADERS = {
        "Content-Type": "application/json ;charset=utf-8 "
    }
    Link_textMsg = {
        "msgtype": "link",
        "link": {
            "text": " https://uploader.shimo.im/f/qtMrUTT2hdQgguKL.png",
            "title": " ",
            "picUrl": "https://uploader.shimo.im/f/qtMrUTT2hdQgguKL.png",
            "messageUrl": "https://uploader.shimo.im/f/qtMrUTT2hdQgguKL.png"
        }
    }
    Link_textMsg = json.dumps(Link_textMsg)
    res = requests.post(url, data=Link_textMsg, headers=HEADERS)
    print(res.text)


def sendmessage_image(access_token, src):
    """
    实现发送图片
    :param access_token:
    :param src:
    :return:
    """
    url = 'https://oapi.dingtalk.com/robot/send?access_token=%s' % (access_token)

    HEADERS = {
        "Content-Type": "application/json ;charset=utf-8 "
    }
    Image_textMsg = {
        "msgtype": "markdown",
        "markdown": {
            "title": "知识点",
            "text": "![](%s)" % src,
        },
        "at": {
            "atMobiles": [
                ""
            ],
            "isAtAll": 0
        }
    }
    Image_textMsg = json.dumps(Image_textMsg)
    res = requests.post(url, data=Image_textMsg, headers=HEADERS)
    print(res.text)


def sendmessage_stop(access_token, ):
    """
    结束语
    :param access_token:
    :return:
    """
    url = 'https://oapi.dingtalk.com/robot/send?access_token=%s' % access_token  # 钉钉机器人的webhook地址
    HEADERS = {
        "Content-Type": "application/json ;charset=utf-8 "
    }
    message = """以上就是我们今天分享的内容"""
    String_textMsg = {
        "msgtype": "text",
        "text": {"content": message},
        "at": {
            "atMobiles": [
                ""  # 如果需要@某人，这里写他的手机号
            ],
            "isAtAll": 1  # 如果需要@所有人，这些写1
        }
    }
    String_textMsg = json.dumps(String_textMsg)
    res = requests.post(url, data=String_textMsg, headers=HEADERS)
    print(res.text)


def crawl_content():
    while not work.empty():
        access_token = work.get_nowait()

        """开局艾特所有人"""
        sendmessage_start(access_token)
        time.sleep(10)

        headers = {
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.92 Safari/537.36',
        }

        res = requests.get(url, headers=headers).content.decode('utf-8')
        bs = BeautifulSoup(res, 'html.parser')

        # 获取标题
        title = bs.find('div', class_='ql-title').find(class_='ql-title-box')['data-value']
        # print(title)
        sendmessage_content(access_token, title)
        # print('-' * 100)
        # 获取内容
        content_list = bs.find('div', class_='ql-editor')
        for content in content_list.children:
            num = random.randint(6, 10)
            try:
                res = content.find('img')
                res = res['src']  # 获取图片链接
                if res:
                    sendmessage_image(access_token, res)
                    # print(res)
                    # print('发送图片')
                    time.sleep(num)
                else:
                    pass
            except Exception as e:
                res = content.text  # 获取正常文字
                if res:
                    # print('************', res)
                    sendmessage_content(access_token, res)
                    time.sleep(num)
                else:
                    pass
        sendmessage_stop(access_token)
        print('')
    print('发送完成')


# def main():
#     # 构造机器人队列
#     access_token_num = int(input('请输入机器人个数：'))
#     work = Queue()
#     for i in range(access_token_num):
#         access_token = input('请输入机器人链接：')
#         work.put_nowait(access_token)
#
#     url = input('请输入石墨链接：')
#
#     # 构造任务列表存放任务
#     tasks_list = []
#     # 协程个数
#     for x in range(access_token_num):
#         task = gevent.spawn(crawl_content)
#         tasks_list.append(task)
#
#     gevent.joinall(tasks_list)

def choose_range():
    """
    选择范围
    :return:
    """
    headers = {
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.92 Safari/537.36',
    }

    url = 'https://shimo.im/docs/j9WHPjkhPkkxHChy'
    res = requests.get(url, headers=headers).content.decode('utf-8')
    bs = BeautifulSoup(res, 'html.parser')

    # with open('shi.html', 'w', encoding='utf-8') as f:
    #     f.write(res)
    content = bs.find('div', class_='ql-editor')
    content_list = content.find_all('p')

    while 1:
        content_url = int(input('请输入知识点分享范围(基础语法输入1，爬虫输入2，数据分析输入3)：'))
        if content_url == 1:
            url = content_list[content_url - 1].find('a')['href']
            break
        elif content_url == 2:
            url = content_list[content_url - 1].find('a')['href']
            break
        elif content_url == 3:
            url = content_list[content_url - 1].find('a')['href']
            break
        else:
            print('输入错误，请重新输入')
            continue
    return url


def choose_chapter(url):
    """
    选择章节
    :param url:
    :return:
    """
    headers = {
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.92 Safari/537.36',
    }
    res = requests.get(url, headers=headers).content.decode('utf-8')
    bs = BeautifulSoup(res, 'html.parser')
    with open('shi.html', 'w', encoding='utf-8') as f:
        f.write(res)
    content = bs.find('div', class_='ql-editor')
    content_list = content.find_all('p')
    # # 选取章节
    # for chapter in content_list:
    #
    #     return chapter.text           # 章节 1  2  3  4  5  6  7  8  9
    chapter = int(input('请输入章节：'))  # 索引 1  3  5  7  9  11
    title = content_list[chapter * 2 - 2].text
    url = content_list[chapter * 2 - 1].find('a')['href']

    return title, url


if __name__ == '__main__':
    while 1:
        choose = input('请输入1开始发送，输入其他退出：')
        if choose == '1':
            print('开始发送')
            access_token_num = int(input('请输入机器人个数：'))
            work = Queue()
            for i in range(access_token_num):
                access_token = input('请输入机器人链接：')
                work.put_nowait(access_token)

            url = choose_range()
            # print(url)
            title, url = choose_chapter(url)
            print('标题', title)
            print('石墨链接', url)

            # 构造任务列表存放任务
            tasks_list = []
            # 协程个数
            for x in range(access_token_num):
                task = gevent.spawn(crawl_content)
                tasks_list.append(task)

            gevent.joinall(tasks_list)
        else:
            break
