# -*- coding: utf-8 -*-
# @Author  : LuoXian
# @Date    : 2020/2/10 16:19
# Software : PyCharm
# version： Python 3.8
# @File    : Bing_relaese.py
import os
import re
import random
import datetime
from urllib.request import urlretrieve
import requests  # pip install requests
from PIL import Image  # pip install pillow 用来显示下载的壁纸


def requests_bing():
    print('开始获取必应每日壁纸!')
    # 请求头
    header = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 \
        (KHTML, like Gecko) Chrome/76.0.3809.132 Safari/537.36',
        'Referer': 'http://bing.ioliu.cn'
    }
    url = 'https://bing.ioliu.cn/'
    # 开始请求
    session = requests.session()
    return session.get(url, headers=header).text  # 返回页面信息


def parse(html):
    # 提取壁纸信息
    data_img = re.findall('data-progressive="(.*?)"', html)
    title = re.findall('<h3>(.*?)\(.*?\)</h3>', html)
    # 随机挑选壁纸
    lucky = random.randint(0, 11)
    return data_img[lucky], title[lucky]  # 返回壁纸的url和标题


def download_img(url, title):
    # 创建壁纸目录
    os.makedirs('Bing壁纸', exist_ok=True)
    os.chdir('Bing壁纸')
    # 以日期为壁纸命名
    today = datetime.datetime.now().date()
    # 下载壁纸
    urlretrieve(url, f'{today}.jpg')
    print(title)
    print('下载壁纸中,很快哟...')
    return os.getcwd() + '/' + str(today) + '.jpg'  # 返回壁纸路径


def show_img(path):
    # 显示壁纸
    img = Image.open(path)
    img.show()


def bing_wallpaper():
    # main 函数
    html = requests_bing()
    url, title = parse(html)
    path = download_img(url, title)
    show_img(path)


if __name__ == '__main__':
    bing_wallpaper()

