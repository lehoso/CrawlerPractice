# -*- coding: utf-8 -*-
# @Author  : LEHOSO
# @FileName: Lianjia2.py
# @Time    : 2021/10/11 16:55

import time

import pandas as pd
import requests
from bs4 import BeautifulSoup

# 表头
header = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) '
                  'AppleWebKit/537.36 (KHTML, like Gecko) '
                  'Chrome/95.0.4638.54 Safari/537.36 Edg/95.0.1020.30'
}
a = []


def get_info(url):
    wb_data = requests.get(url, headers=header)
    # 爬取整个网页
    soup = BeautifulSoup(wb_data.text, 'lxml')
    # 网页单个元素
    ranks = soup.select('div.totalPrice.totalPrice2 > span')
    title = soup.select('div.title > a')
    location = soup.select('div.flood > div > a')
    area = soup.select('div.flood > div > a:nth-child(3)')
    fllowInfo = soup.select('div.followInfo')
    # 存入进列表
    for ranks, titles, locaitons, areas, fllowInfos in zip(ranks, title, location, area, fllowInfo):
        data = {
            '价格': ranks.get_text().strip(),
            '标题': titles.get_text().strip(),
            '位置': locaitons.get_text().strip() + '-' + areas.get_text().strip(),
            '关注': fllowInfos.get_text().strip().split('/')[0],
            '距今发布日期': fllowInfos.get_text().strip().split('/')[1]
        }
        a.append(data)
        print(data)


if __name__ == '__main__':
    # 网址路径
    urls = [
        'https://cq.lianjia.com/ershoufang/'
    ]
    for url in urls:
        get_info(url)
        time.sleep(2)
    # pandas存入数据
    df_out = pd.DataFrame(a, columns=['价格', '标题', '位置', '关注', '距今发布日期'])
    df_out.to_excel('aaa.xlsx')
