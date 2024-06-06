import re
import time

import pandas as pd
import requests
from bs4 import BeautifulSoup

b = []


def get_html(url):
    # url = "https://anshan.anjuke.com/community/p1"

    payload = {}
    headers = {
        'Cookie': 'Cookie=sessid=B8EDC173-F262-AA43-02EF-FF82950E2BD9; aQQ_ajkguid=B937A289-AAD3-C14A-311C-E38CC41A793B; twe=2; ajk-appVersion=; id58=CrIW6mZf7liYqGPjGb93Ag==; isp=true; 58tj_uuid=da66cb15-a4f9-4ce6-b201-ed4afc2a4aac; xxzlclientid=c9503abf-1d2c-418c-b736-1717563229691; xxzlxxid=pfmxR+94+OV9CbCo7QUVMJ5AXt+MaBFd0vb76A58s9iZSTZ+fJHZqJMG5UMzPqfh8aXc; als=0; lps=https%3A%2F%2Fheb.zu.anjuke.com%2F%3Ffrom%3DHomePage_TopBar%7Chttps%3A%2F%2Fheb.anjuke.com%2F; cmctid=202; xxzlbbid=pfmbM3wxMDM1MXwxLjguMXwxNzE3NTczMzI2ODkyfG52MmsrQzRxRVd0MDBRUlJqbXl4eGhSMzQzU1poRk1UL2J2UTIyc1B3d3c9fDM1YWNjNWNhYzNhODc5YzA1MGFiNDQ3YjkzYzEzMTE4XzE3MTc1NzMzMzI1ODFfZmJhMGY5NTYzODdhNDAwODk1ZTg4YzQ3ZDlkNzRlZjVfMTAzMTg0ODczM3w3YzUwNWQ2N2E5YTJmMGM1ODk3ZWQ1Yjk3YzQyMzUyY18xNzE3NTczMzI2NDEyXzI1Ng==; ajk_member_verify=ZtrRHaydORjVQQetzDoL0XZIcdPlU5pHNf3lLFLu%2BQE%3D; ajk_member_verify2=MjIxMzk0MzI4fG00ZmRFOWp8MQ%3D%3D; ajk_member_id=221394328; _ga=GA1.2.191220906.1717596493; _gid=GA1.2.328357475.1717596493; ctid=107; fzq_js_anjuke_ershoufang_pc=e1b6b76d9855346aaa16bc3e46e3c1d5_1717646397861_23; fzq_h=c637c6f935a737fac67633c5772f2ec6_1717654388389_ef3893beda1447e7a057dc3ecefb3629_1031848733; obtain_by=2; init_refer=; new_uv=4; new_session=0; _ga_DYBJHZFBX2=GS1.2.1717668257.3.1.1717668262.0.0.0; xxzl_cid=2e6674b9aea04847ba1e6fa67c22f0a1; xxzl_deviceid=vPdWPVihxf/xpDuLLfvFu+u8fyA52RZ3De7pK4LLtwGz1paKchpLJfmfpgvRYT2v; ajkAuthTicket=TT=fc173b2c99a2f1b982ade3fe69c8cb2c&TS=1717668513971&PBODY=Qn55fr3HX9fuQYI8eQq1z7GrrpgFmwBMxqkjJWF7_phPtHK3lKllT1RDKYwWKbZwBzrKSh6drXpEUGdNZ_OfixJ0VxKUlb9CJFLqjyXBpi1nx9e3NGxZOkSntdCCCCAPW9b-BSXbBiNiKtaNpCfrSaQXgsrZRg6N_Tc1uLS8J_U&VER=2&CUID=4eGSxIUoYdqQQOls3Krf9aS2r3T3qS61; fzq_js_anjuke_xiaoqu_pc=466a010dc0348dfd756cc14bc32e6d72_1717668508212_25; sessid=4E80504B-10B8-6EDC-43E9-6B8921CB84D4; aQQ_ajkguid=93AC710A-9B2E-0C2A-CD34-19BD539D52C6; ctid=107; obtain_by=1; twe=2; ajk-appVersion=; fzq_h=6f283aabdfcb6686f282e399ef8ad147_1717659954700_0eb1c3e3ee5e486ea638ad73b6092d34_1031848733',
        'User-Agent': 'Apifox/1.0.0 (https://apifox.com)',
        'Accept': '*/*',
        'Host': 'anshan.anjuke.com',
        'Connection': 'keep-alive'
    }

    response = requests.request("GET", url, headers=headers, data=payload)
    # print(response.text)
    html_content = response.text
    # print(html_content)
    # with open("anshan.html", "w", encoding="utf-8") as file:
    #     file.write(html_content)
    #
    # # 使用BeautifulSoup解析保存的HTML文件
    # with open("anshan.html", "r", encoding="utf-8") as file:
    #     soup = BeautifulSoup(file, 'html.parser')
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
            '链接': href,
            '总数': inside,
            '小区名': title,
        }
        b.append(data)
        page_community_total += 1
        print(f'链接: {href},  总数: {inside},小区名:{title}')
    return total_community, page_community_total


if __name__ == '__main__':
    # 总条数
    total = 0
    # 获取的总数
    get_city_total = 0
    page_num = 1
    # 小区最多显示50页
for page in range(0, 50):
    if get_city_total != 0 and get_city_total >= total:
        break
    url = 'https://anshan.anjuke.com/community/p' + str(page_num)
    data_total, page_total = get_html(url)
    # 每页数据获取
    get_city_total += int(page_total)
    total = int(data_total)
    print(f'页数：{page_num}，条数：{data_total}，已获取条数{get_city_total}')
    time.sleep(3)
    page_num += 1

df_out = pd.DataFrame(b, columns=['链接',
                                  '总数',
                                  '小区名'
                                  ])
df_out.to_excel('测试数据鞍山.xlsx')
