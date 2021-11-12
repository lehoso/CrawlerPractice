# -*- coding: utf-8 -*-
# @Author  : LEHOSO
# @FileName: Kugou.py
# @Time    : 2021/10/11 16:55

import time

import pandas as pd
import requests
from bs4 import BeautifulSoup

header = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) '
                  'AppleWebKit/537.36 (KHTML, like Gecko) '
                  'Chrome/95.0.4638.54 Safari/537.36 Edg/95.0.1020.30'
}
a = []


def get_info(url):
    wb_data = requests.get(url, headers=header)
    soup = BeautifulSoup(wb_data.text, 'lxml')
    ranks = soup.select(
        '#content > div.leftContent > ul > li > div.info.clear > div.priceInfo > div.totalPrice.totalPrice2 > span')
    title = soup.select('#content > div.leftContent > ul > li > div.info.clear > div.title > a')
    location = soup.select('#content > div.leftContent > ul > li > div.info.clear > div.flood > div > a')
    area = soup.select('#content > div.leftContent > ul > li> div.info.clear > div.flood > div > a:nth-child(3)')
    fllowInfo = soup.select('#content > div.leftContent > ul > li > div.info.clear > div.followInfo')
    for rank, title, locaiton, area, fllowInfo in zip(ranks, title, location, area, fllowInfo):
        data = {
            '价格': rank.get_text().strip(),
            '标题': title.get_text().strip(),
            '位置': locaiton.get_text().strip() + '-' + area.get_text().strip(),
            '关注': fllowInfo.get_text().strip().split('/')[0],
            '距今发布日期': fllowInfo.get_text().strip().split('/')[1]
        }
        a.append(data)
        print(data)


if __name__ == '__main__':
    urls = [
        'https://cq.lianjia.com/ershoufang/'
    ]
    for url in urls:
        get_info(url)
        time.sleep(2)
    df_out = pd.DataFrame(a, columns=['价格', '标题', '位置', '关注', '距今发布日期'])
    df_out.to_excel('aaa.xlsx')
