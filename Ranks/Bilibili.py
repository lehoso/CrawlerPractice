# -*- coding: utf-8 -*-
# @Author  : LEHOSO
# @FileName: Bilibili.py
# @Time    : 2021/10/11 16:52
import requests
from bs4 import BeautifulSoup

url = 'https://www.bilibili.com/v/popular/rank/all'  # 爬取B站排行榜（总榜）上视频链接
res = requests.get(url)
soup = BeautifulSoup(res.text, 'lxml')
# 定义列表来存储数据
Author = []  # 作者
URL = []  # 链接
Name = []  # 标题
pts = []  # 综合评分
# 利用bs4，找到视频链接以及视频名字和up主
get_Author = soup.find_all('span', class_='data-box up-name')
get_url = soup.find_all('a', class_="title")
get_Pts = soup.find_all('div', class_='pts')
# 将数据存入列表中
for data in get_Author:
    author = data.text.replace('\n', '').replace(' ', '')
    Author.append(author)
for item in get_url:
    URL.append(item['href'].replace('//', 'https://'))  # 找到链接并转换成链接形式
    Name.append(item.text)

for ComprehensiveScore in get_Pts:
    PTS = ComprehensiveScore.text.replace('\n', '').replace(' ', '').replace('综合得分', '')
    pts.append(PTS)

# 将数据写入文件中保存下来
header = ['作品名', '作者', '作品链接', '综合评分']
headers = ','.join(header)
date = (list(z) for z in zip(Name, Author, URL, pts))  # 把数据成组，方便写入文件。
with open("排行榜数据.csv", 'w+', encoding='utf-8') as f:
    f.write(headers + '\n')
    for i in date:
        i = ','.join(i)  # 将列表转为字符串
        f.writelines(i + '\n')
print('{:*^30}'.format('保存成功！'))
