# -*- coding: utf-8 -*-
# @Author  : LEHOSO
# @FileName: Kugou.py
# @Time    : 2021/10/11 16:55

import time

import pandas as pd
import requests
from bs4 import BeautifulSoup

#表头
header = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) '
                  'AppleWebKit/537.36 (KHTML, like Gecko) '
                  'Chrome/94.0.4606.71 Safari/537.36 Edg/94.0.992.38'
}
a = []

#获取标题，时间
def get_info(url):
    wb_data = requests.get(url, headers=header)
    soup = BeautifulSoup(wb_data.text, 'lxml')
    ranks = soup.select('span.pc_temp_num')
    titles = soup.select('div.pc_temp_songlist > ul > li > a')
    times = soup.select('span.pc_temp_tips_r > span')
    for rank, title, time in zip(ranks, titles, times):
        strl = title.get_text().split(',')
        data = {
            'rank': rank.get_text().strip(),
            'singer': strl[0],
            'song': strl[-1],
            'time': time.get_text().strip()
        }
        #追加数据
        a.append(data)
        print(data)

if __name__ == '__main__':
    #位置在酷狗音乐排行榜单
    urls = [
        'https://www.kugou.com/yy/rank/home/{}.8888.html'.format(str(i) for i in range(1, 2))
    ]
    for url in urls:
        get_info(url)
        time.sleep(2)
    df_out = pd.DataFrame(a, columns=['rank', 'singer', 'song', 'time'])
    df_out.to_excel('aaa.xlsx')
