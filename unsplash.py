# _*_ coding:utf-8 _*_

import requests
import math
import json
import os
from requests.packages import urllib3

# 获取页面Response
def getHtmlResponse(url):
    headers = {
    'User-Agent':'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.149 Safari/537.36 Edg/80.0.361.69',
    'Referer': 'https://unsplash.com/'
    }

    try:
        urllib3.disable_warnings()
        r = requests.get(url,verify=False,headers=headers)
        r.raise_for_status()
        r.encoding = r.apparent_encoding
        return r
    except Exception as e:
        return ''

# 下载一张图片
def getPicture(url,path,name):
    try:
        req = getHtmlResponse(url)
        if not os.path.exists(path):
            os.makedirs(path)
        with open(path+name,'wb') as f:
            f.write(req.content)
            f.flush()
    except Exception as e:
        return ''

# 下载一页20张图片
def getOnePage(url,path):
    req = getHtmlResponse(url)
    html = req.text
    data = json.loads(html)
    # getPicture(url)
    count = 0
    for result in data['results']:
        count = count + 1
        # 获取“alt_description”命名文件
        name = result['alt_description']+'.jpg'
        # 获取下载链接，并确定下载尺寸，这里选定宽度为2400,还有1920
        pic_url = result['links']['download']+'?force=true&w=2400'
        print('正在下载第%d张照片：%s……' % (count,name))
        getPicture(pic_url,path,name)

# 主函数
if __name__ == '__main__':
    theme = input('请输入要下载的照片主题：')  # great-wall-of-china,china
    path = theme + '/'
    num = int(input('请输入下载数量：'))
    page_num = math.ceil(num/20)

    for i in range(1,page_num+1):
        url = 'http://unsplash.com/napi/search/photos?query='+theme+'&per_page=20&page='+str(i)
        getOnePage(url,path)
        print('第'+ i +'页下载完毕')

    print('%d张%s主题的照片全部下载完成！' % (num,theme))
