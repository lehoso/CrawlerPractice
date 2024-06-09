import http.client
import re
import time
from urllib.parse import urlparse

import pandas as pd
import requests
from bs4 import BeautifulSoup

'''
详细链接
'''

a = []

error_data = []


def get_community_html(url, city_name, community_name):
    payload = {}
    parsed_url = urlparse(url)
    headers = {
        'Cookie': 'sessid=B8EDC173-F262-AA43-02EF-FF82950E2BD9; aQQ_ajkguid=B937A289-AAD3-C14A-311C-E38CC41A793B; twe=2; ajk-appVersion=; id58=CrIW6mZf7liYqGPjGb93Ag==; isp=true; 58tj_uuid=da66cb15-a4f9-4ce6-b201-ed4afc2a4aac; xxzlclientid=c9503abf-1d2c-418c-b736-1717563229691; xxzlxxid=pfmxR+94+OV9CbCo7QUVMJ5AXt+MaBFd0vb76A58s9iZSTZ+fJHZqJMG5UMzPqfh8aXc; als=0; lps=https%3A%2F%2Fheb.zu.anjuke.com%2F%3Ffrom%3DHomePage_TopBar%7Chttps%3A%2F%2Fheb.anjuke.com%2F; cmctid=202; xxzlbbid=pfmbM3wxMDM1MXwxLjguMXwxNzE3NTczMzI2ODkyfG52MmsrQzRxRVd0MDBRUlJqbXl4eGhSMzQzU1poRk1UL2J2UTIyc1B3d3c9fDM1YWNjNWNhYzNhODc5YzA1MGFiNDQ3YjkzYzEzMTE4XzE3MTc1NzMzMzI1ODFfZmJhMGY5NTYzODdhNDAwODk1ZTg4YzQ3ZDlkNzRlZjVfMTAzMTg0ODczM3w3YzUwNWQ2N2E5YTJmMGM1ODk3ZWQ1Yjk3YzQyMzUyY18xNzE3NTczMzI2NDEyXzI1Ng==; ajk_member_verify=ZtrRHaydORjVQQetzDoL0XZIcdPlU5pHNf3lLFLu%2BQE%3D; ajk_member_verify2=MjIxMzk0MzI4fG00ZmRFOWp8MQ%3D%3D; ajk_member_id=221394328; _ga=GA1.2.191220906.1717596493; new_uv=5; _ga_DYBJHZFBX2=GS1.2.1717683580.4.0.1717683580.0.0.0; fzq_h=5643a6d45f8670914b51a805ef3818e8_1717849347990_0c0b6c8be6c34b5b9980c3ddd74a1f93_1031848733; fzq_js_anjuke_ershoufang_pc=034353a8311dcce9aef8976c9e0c802a_1717911109608_25; obtain_by=2; ctid=128; xxzl_cid=38d85cfe6dec4298be0f4acaa3f6924a; xxzl_deviceid=79zLeHNhROJJUjkSislV8bFzRvMJfksQ5xOYOZKGKJjNWvJlHleqo/irvPnNNzrb; ajkAuthTicket=TT=fc173b2c99a2f1b982ade3fe69c8cb2c&TS=1717915364126&PBODY=m6SNH9hCi5xxIuxynVrPlZhEmqwP4ICN2bk8s_j0uSReuSbOQVNrddTFXiC7kB1U9CJJDvsFft3RZpARS-ZWn8CtepxCM2l0BoVlD5C2HN8hdlTBFvhCyULh9MghT9FyNpQEMa5j4hOgwDWF9_qRc2gmRX3oq4f4RuxF5T0XnK8&VER=2&CUID=4eGSxIUoYdqQQOls3Krf9aS2r3T3qS61; fzq_js_anjuke_xiaoqu_pc=28a750fb7fc7ba4a7aa28d8e4bc05408_1717915355541_24',
        'User-Agent': 'Apifox/1.0.0 (https://apifox.com)',
        'Accept': '*/*',
        'Host': parsed_url.hostname,
        'Connection': 'keep-alive'
    }
    response = requests.request("GET", url, headers=headers, data=payload)
    html_content = response.text
    soup = BeautifulSoup(html_content, 'lxml')
    selector = "#__layout > div > section > section.list-main > section > section:nth-child(2) > div:nth-child(n) > a"
    tags = soup.select(selector)

    community_detail = 0
    # 输出每个匹配的a标签的href属性
    for tag in tags:
        if tag and 'href' in tag.attrs:
            title = tag.find('h3', class_='property-content-title-name').contents[0].strip()
            href = tag['href']
            print(f'要抓取的链接：{href}')
            retries = 5
            while retries > 0:
                try:
                    data = {
                        '城市': city_name,
                        '小区': community_name,
                        '链接': href,
                        '标题': title
                    }
                    a.append(data)
                    break
                except Exception as e:
                    retries -= 1
                    print(f'获取{row["城市"]}第{href}链接。重试中...（剩余重试次数：{retries}）')
                    error_data.append(href)
                    print(f'异常信息：{e}')
            community_detail += 1
        else:
            print("未找到标签或标签不包含href属性。")
    return community_detail


not_data = []

if __name__ == '__main__':
    df = pd.read_excel('所有小区.xlsx')
    for index, row in df.iterrows():
        # 总条数
        total = row["总数"]
        # 获取的总数
        get_community_total = 0
        print(f'城市：{row["城市"]}，链接：{row["链接"]}，小区名{row["小区名"]}，总数{total}')
        page_num = 1
        for page in range(0, 50):
            if get_community_total != 0 and get_community_total >= total:
                break
            # 每个小区的详情
            url = row["链接"] + 'p' + str(page_num)
            retries = 5
            while retries > 0:
                try:
                    # 该分页获取的总数
                    community_detail = get_community_html(url, row["城市"], row["小区名"])
                    # 每页数据获取
                    if int(community_detail) == 0:
                        not_data.append(url)
                        raise Exception("发现空数据。可能需要验证")
                    get_community_total += community_detail
                    print(f'页数：{page_num}，已获取条数{community_detail},已获取总条数：{get_community_total}，全部总条数：{total}')
                    page_num += 1
                    break
                except Exception as e:
                    retries -= 1
                    print(f'获取{row["城市"]}第{page_num}页数据时发生错误。重试中...（剩余重试次数：{retries}）')
                    print(f'异常信息：{e}')
            # time.sleep(1)
    df_out = pd.DataFrame(a, columns=['城市', '小区', '链接', '标题'])
    df_out.to_excel('每个小区的所有二手房连接.xlsx')
    print(f'空数据：{not_data}')
    print(f'链接获取错误数据：{error_data}')
