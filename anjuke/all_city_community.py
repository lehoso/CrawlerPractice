# 所有城市的小区
import re
import time
from urllib.parse import urlparse

import pandas as pd
import requests
from bs4 import BeautifulSoup

result = []
all_city = {
    'daqing.anjuke.com': '大庆',
    'datong.anjuke.com': '大同',
    'gannan.anjuke.com': '甘南',
    'heb.anjuke.com': '哈尔滨',
    'hegang.anjuke.com': '鹤岗',
    'heihe.anjuke.com': '黑河',
    'jiamusi.anjuke.com': '佳木斯',
    'jixi.anjuke.com': '鸡西',
    'mudanjiang.anjuke.com': '牡丹江',
    'qiqihaer.anjuke.com': '齐齐哈尔',
    'qitaihe.anjuke.com': '七台河',
    'shanda.anjuke.com': '安达',
    'shuangyashan.anjuke.com': '双鸭山',
    'shzhaodong.anjuke.com': '肇东',
    'suihua.anjuke.com': '绥化',
    'xa.anjuke.com': '西安',
    'yichunshi.anjuke.com': '伊春',
    'zhaozhou.anjuke.com': '肇州'}


def get_html(url, city_name):
    # url = "https://anshan.anjuke.com/community/p1"

    payload = {}
    parsed_url = urlparse(url)
    headers = {
        'Cookie': 'sessid=B8EDC173-F262-AA43-02EF-FF82950E2BD9; aQQ_ajkguid=B937A289-AAD3-C14A-311C-E38CC41A793B; twe=2; ajk-appVersion=; id58=CrIW6mZf7liYqGPjGb93Ag==; isp=true; 58tj_uuid=da66cb15-a4f9-4ce6-b201-ed4afc2a4aac; xxzlclientid=c9503abf-1d2c-418c-b736-1717563229691; xxzlxxid=pfmxR+94+OV9CbCo7QUVMJ5AXt+MaBFd0vb76A58s9iZSTZ+fJHZqJMG5UMzPqfh8aXc; als=0; lps=https%3A%2F%2Fheb.zu.anjuke.com%2F%3Ffrom%3DHomePage_TopBar%7Chttps%3A%2F%2Fheb.anjuke.com%2F; cmctid=202; xxzlbbid=pfmbM3wxMDM1MXwxLjguMXwxNzE3NTczMzI2ODkyfG52MmsrQzRxRVd0MDBRUlJqbXl4eGhSMzQzU1poRk1UL2J2UTIyc1B3d3c9fDM1YWNjNWNhYzNhODc5YzA1MGFiNDQ3YjkzYzEzMTE4XzE3MTc1NzMzMzI1ODFfZmJhMGY5NTYzODdhNDAwODk1ZTg4YzQ3ZDlkNzRlZjVfMTAzMTg0ODczM3w3YzUwNWQ2N2E5YTJmMGM1ODk3ZWQ1Yjk3YzQyMzUyY18xNzE3NTczMzI2NDEyXzI1Ng==; ajk_member_verify=ZtrRHaydORjVQQetzDoL0XZIcdPlU5pHNf3lLFLu%2BQE%3D; ajk_member_verify2=MjIxMzk0MzI4fG00ZmRFOWp8MQ%3D%3D; ajk_member_id=221394328; _ga=GA1.2.191220906.1717596493; new_uv=5; _ga_DYBJHZFBX2=GS1.2.1717683580.4.0.1717683580.0.0.0; fzq_h=5643a6d45f8670914b51a805ef3818e8_1717849347990_0c0b6c8be6c34b5b9980c3ddd74a1f93_1031848733; ctid=205; fzq_js_anjuke_ershoufang_pc=c94259d220e5d2c2cfcf68d27e252357_1717855659653_25; obtain_by=2; xxzl_cid=38d85cfe6dec4298be0f4acaa3f6924a; xxzl_deviceid=79zLeHNhROJJUjkSislV8bFzRvMJfksQ5xOYOZKGKJjNWvJlHleqo/irvPnNNzrb; ajkAuthTicket=TT=fc173b2c99a2f1b982ade3fe69c8cb2c&TS=1717855674576&PBODY=gFeTnb7UZTEyhztZXLAbCa_CetQ8FjkyNwUmm8JaFVeFEwUOAhCQ9_wk8kOEVvbdju8w9nRQvdHs6j7-JOa3o4VP8XpidXqRtJHr-NcdgAWEcWON-XeMvL8EegVc5jmb0dZzByJ_IFQ6Md1FW80I9R0nLeiERJDBQq0NSMx1dCE&VER=2&CUID=4eGSxIUoYdqQQOls3Krf9aS2r3T3qS61; fzq_js_anjuke_xiaoqu_pc=9f0bf8d40423cb275f5baa413196c3bd_1717855665825_24',
        'User-Agent': 'Apifox/1.0.0 (https://apifox.com)',
        'Accept': '*/*',
        'Host': parsed_url.hostname,
        'Connection': 'keep-alive'
    }

    response = requests.request("GET", url, headers=headers, data=payload)
    # print(response.text)

    html_content = response.text
    soup = BeautifulSoup(html_content, 'html.parser')
    total_community = soup.find('div', class_='sort-row').find('span', class_='total-info').text
    total_community = re.sub("\\D", "", total_community)
    #  总共多少小区
    print(total_community)

    second_hand_homes = soup.find('div', class_='list-cell').findAll('a', class_='li-row')
    page_community_total = 0
    for second_hand_home in second_hand_homes:
        title = second_hand_home.find('div', class_='nowrap-min li-community-title').text
        home = second_hand_home.find('span', class_='detail-link').find('a')
        # 小区廉洁
        href = home.get('href')
        ##小区二手房数量
        text = home.text
        # 使用正则表达式提取括号内和括号外的字符
        match = re.match(r'([^()]+)\(([^()]+)\)', text)
        if match:
            outside, inside = match.groups()

        data = {
            '城市': city_name,
            '链接': href,
            '总数': inside,
            '小区名': title,
        }
        result.append(data)
        page_community_total += 1
        print(f'城市:{city_name},链接: {href},  总数: {inside},小区名:{title}')
    return total_community, page_community_total


if __name__ == '__main__':
    # 小区最多显示50页
    for city in all_city:
        # 总条数
        total = 0
        # 获取的总数
        get_city_total = 0
        page_num = 1
        for page in range(0, 50):
            if get_city_total != 0 and get_city_total >= total:
                break

            url = 'https://' + city + '/community/p' + str(page_num)
            retries = 5
            while retries > 0:
                try:
                    data_total, page_total = get_html(url, all_city[city])
                    # 每页数据获取
                    get_city_total += int(page_total)
                    total = int(data_total)
                    print(f'页数：{page_num}，条数：{data_total}，已获取条数{get_city_total}')
                    page_num += 1
                    time.sleep(3)
                    break
                except Exception as e:
                    retries -= 1
                    print(f'获取{city}第{page_num}页数据时发生错误。重试中...（剩余重试次数：{retries}）')
                    print(f'异常信息：{e}')
            else:
                print(f'多次重试后无法获取{city}第{page_num}页的数据。')
                break  # 可选：在多次重试失败后退出循环
    df_out = pd.DataFrame(result, columns=['城市', '链接', '总数', '小区名'])
    df_out.to_excel('城市.xlsx')
