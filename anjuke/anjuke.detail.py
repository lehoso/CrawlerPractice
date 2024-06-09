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


def get_detail(city, url):
    print("当前链接：" + url)
    parsed_url = urlparse(url)
    conn = http.client.HTTPSConnection(parsed_url.hostname)
    payload = ''
    headers = {
        'Cookie': 'sessid=B8EDC173-F262-AA43-02EF-FF82950E2BD9; aQQ_ajkguid=B937A289-AAD3-C14A-311C-E38CC41A793B; twe=2; ajk-appVersion=; id58=CrIW6mZf7liYqGPjGb93Ag==; isp=true; 58tj_uuid=da66cb15-a4f9-4ce6-b201-ed4afc2a4aac; xxzlclientid=c9503abf-1d2c-418c-b736-1717563229691; xxzlxxid=pfmxR+94+OV9CbCo7QUVMJ5AXt+MaBFd0vb76A58s9iZSTZ+fJHZqJMG5UMzPqfh8aXc; als=0; lps=https%3A%2F%2Fheb.zu.anjuke.com%2F%3Ffrom%3DHomePage_TopBar%7Chttps%3A%2F%2Fheb.anjuke.com%2F; cmctid=202; xxzlbbid=pfmbM3wxMDM1MXwxLjguMXwxNzE3NTczMzI2ODkyfG52MmsrQzRxRVd0MDBRUlJqbXl4eGhSMzQzU1poRk1UL2J2UTIyc1B3d3c9fDM1YWNjNWNhYzNhODc5YzA1MGFiNDQ3YjkzYzEzMTE4XzE3MTc1NzMzMzI1ODFfZmJhMGY5NTYzODdhNDAwODk1ZTg4YzQ3ZDlkNzRlZjVfMTAzMTg0ODczM3w3YzUwNWQ2N2E5YTJmMGM1ODk3ZWQ1Yjk3YzQyMzUyY18xNzE3NTczMzI2NDEyXzI1Ng==; ajk_member_verify=ZtrRHaydORjVQQetzDoL0XZIcdPlU5pHNf3lLFLu%2BQE%3D; ajk_member_verify2=MjIxMzk0MzI4fG00ZmRFOWp8MQ%3D%3D; ajk_member_id=221394328; _ga=GA1.2.191220906.1717596493; new_uv=5; _ga_DYBJHZFBX2=GS1.2.1717683580.4.0.1717683580.0.0.0; fzq_h=5643a6d45f8670914b51a805ef3818e8_1717849347990_0c0b6c8be6c34b5b9980c3ddd74a1f93_1031848733; ctid=205; fzq_js_anjuke_ershoufang_pc=c94259d220e5d2c2cfcf68d27e252357_1717855659653_25; obtain_by=2; xxzl_cid=38d85cfe6dec4298be0f4acaa3f6924a; xxzl_deviceid=79zLeHNhROJJUjkSislV8bFzRvMJfksQ5xOYOZKGKJjNWvJlHleqo/irvPnNNzrb; ajkAuthTicket=TT=fc173b2c99a2f1b982ade3fe69c8cb2c&TS=1717855674576&PBODY=gFeTnb7UZTEyhztZXLAbCa_CetQ8FjkyNwUmm8JaFVeFEwUOAhCQ9_wk8kOEVvbdju8w9nRQvdHs6j7-JOa3o4VP8XpidXqRtJHr-NcdgAWEcWON-XeMvL8EegVc5jmb0dZzByJ_IFQ6Md1FW80I9R0nLeiERJDBQq0NSMx1dCE&VER=2&CUID=4eGSxIUoYdqQQOls3Krf9aS2r3T3qS61; fzq_js_anjuke_xiaoqu_pc=9f0bf8d40423cb275f5baa413196c3bd_1717855665825_24',
        'User-Agent': 'Apifox/1.0.0 (https://apifox.com)',
        'Accept': '*/*',
        'Host': parsed_url.hostname,
        'Connection': 'keep-alive'
    }
    # conn.request("GET",
    #              "https://heb.anjuke.com/prop/view/S3375048294555659?auction=221&hpType=27&entry=136&position=0&kwtype=comm_one&now_time=1717587102&spread=commsearch_c&epauction=&stats_key=bf39dc73-9a23-430f-ae20-76fadb2aed58_0&from=PC_COMM_ESF_LIST_CLICK&index=0",
    #              payload, headers)
    conn.request("GET", url, payload, headers)
    res = conn.getresponse()
    data = res.read()
    # print(data.decode("utf-8"))
    html_content = data.decode("utf-8")
    # with open("S2754299020782597.html", "w", encoding="utf-8") as file:
    #     file.write(html_content)
    # with open("S2754299020782597.html", "r", encoding="utf-8") as file:
    #     soup = BeautifulSoup(file, 'lxml')
    soup = BeautifulSoup(html_content, 'lxml')
    # 行政区
    district = soup.select('#__layout > div > div.props-main > div.props-body > div.props-right > div.maininfo > div.maininfo-meta >'
                           ' div.maininfo-community > div:nth-child(2) > span.maininfo-community-item-name > a:nth-child(1)')
    district = district[0].get_text() if len(district) != 0 else ''
    #  print("行政区：" + district.get_text())
    # 所属区域
    region = soup.select('#__layout > div > div.props-main > div.props-body > div.props-right > div.maininfo > div.maininfo-meta >'
                         ' div.maininfo-community > div:nth-child(2) > span.maininfo-community-item-name > a:nth-child(2)')
    region = region[0].get_text() if len(region) != 0 else ''

    #  print("所属区域：" + region.get_text())
    # 小区名称
    community_name = soup.select('#__layout > div > div.props-main > div.banner > div.banner-breadCrumbs > div > a:nth-child(5)')
    community_name = community_name[0].get_text() if len(community_name) != 0 else ''

    #  print("小区名称:" + community_name.get_text())
    # 地址
    # 建筑面积（㎡）
    area = soup.select(
        '#__layout > div > div.props-main > div.props-body > div.props-right > div.maininfo > '
        'div.maininfo-model > div.maininfo-model-item.maininfo-model-item-2 > div.maininfo-model-strong > i')
    area = area[0].get_text() if len(area) != 0 else ''

    #  print("建筑面积" + area.get_text())
    floors = soup.find('div', class_='maininfo-model-weak')
    floors = floors.text if floors != None != 0 else ''
    # 使用正则表达式提取括号内和括号外的字符
    match = re.match(r'([^()]+)\(([^()]+)\)', floors)
    outside = ''
    inside = ''
    if match:
        outside, inside = match.groups()
        # 所在层
    #  print("楼层等级:", outside)
    # 总层数
    #  print("总共层数:", inside)
    else:
        inside = floors
        print("未匹配到有效格式的字符串")
    # 房屋户型
    house_type = soup.find('div', class_='maininfo-model-strong')
    house_type = house_type.text if house_type is not None else ''
    # 户型结构
    # 房屋结构
    # 装修状况
    renovation_condition = soup.select('#__layout > div > div.props-main > div.props-body > div.props-right > div.maininfo > div.maininfo-model > '
                                       'div.maininfo-model-item.maininfo-model-item-2 > div.maininfo-model-weak')
    renovation_condition = renovation_condition[0].get_text() if len(renovation_condition) != 0 else ''

    #  print("装修状况：" + renovation_condition.get_text())
    # 建筑形式

    purpose_year = soup.select(
        '#__layout > div > div.props-main > div.props-body > div.props-right > div.maininfo > div.maininfo-model > '
        'div.maininfo-model-item.maininfo-model-item-3 > div.maininfo-model-weak')
    purpose_year = purpose_year[0].get_text() if len(purpose_year) != 0 else ''

    # print(purpose_year.get_text())
    # 以“/”分割字符串，并保留两个部分
    parts = purpose_year.split('/')

    if len(parts) == 2:
        part1, part2 = parts
    else:
        part1, part2 = parts, None
    # 房屋用途
    #  print("房屋用途:", part1)
    # 建成年份
    #  print("建成年份:", part2 if part2 else "无")

    # 房屋朝向
    asaga = soup.select('#__layout > div > div.props-main > div.props-body > div.props-right > div.maininfo > div.maininfo-model > '
                        'div.maininfo-model-item.maininfo-model-item-3 > div.maininfo-model-strong > i')
    asaga = asaga[0].get_text() if len(asaga) != 0 else ''

    #  print("房屋朝向：" + asaga.get_text())
    # 楼户比例
    # 发布时间
    released = soup.select('#houseInfo > table > tbody > tr:nth-child(7) > td.houseInfo-main-item-first > span.houseInfo-main-item-name')
    released = released[0].get_text() if len(released) != 0 else ''

    # 营业执照
    license = soup.select('houseInfo > table > tbody > tr:nth-child(6) > td.houseInfo-main-item-first > span.houseInfo-main-item-name')
    license = license[0].get_text() if len(license) != 0 else ''

    #  print("发布时间：" + released.get_text())
    # 更新时间
    update_time = soup.select('#houseInfo > table > tbody > tr:nth-child(7) > td.houseInfo-main-item-first > span.houseInfo-main-item-name')
    update_time = update_time[0].get_text() if len(update_time) != 0 else ''

    #  print("更新时间：" + update_time.get_text())
    # 经纪公司
    brokerage_firms = soup.select(
        '#__layout > div > div.props-main > div.props-body > div.props-right > div.maininfo > div.maininfo-broker > div.maininfo-broker-info > div.maininfo-broker-info-company > div > a')
    brokerage_firms = brokerage_firms[0].get_text().strip() if len(brokerage_firms) != 0 else ''
    #  print("经纪公司：" + brokerage_firms.get_text())
    # 经纪人
    broker = soup.select('#__layout > div > div.props-main > div.props-body > div.props-right > div.maininfo > div.maininfo-broker > '
                         'div.maininfo-broker-info > div.maininfo-broker-info-title > div.maininfo-broker-info-name')
    broker = broker[0].get_text() if len(broker) != 0 else ''
    #  print("经纪人" + broker.get_text())
    # 房本年限
    bomoto_term = soup.select('#houseInfo > table > tbody > tr:nth-child(2) > td.houseInfo-main-item-first > span.houseInfo-main-item-name')
    bomoto_term = bomoto_term[0].get_text() if len(bomoto_term) != 0 else ''

    #  print("房本年限:" + bomoto_term.get_text())
    # 产权所属

    # 产权类型
    property_rights = soup.select('#houseInfo > table > tbody > tr:nth-child(1) > td.houseInfo-main-item-first > span.houseInfo-main-item-name')
    property_rights = property_rights[0].get_text() if len(property_rights) != 0 else ''

    #  print("产权所属：" + property_rights.get_text())
    # 有无大税
    # 房龄
    house_age = soup.select('#houseInfo > table > tbody > tr:nth-child(2) > td:nth-child(3) > span.houseInfo-main-item-name')
    house_age = house_age[0].get_text() if len(house_age) != 0 else None

    #  print("房龄：" + house_age.get_text())
    # 小区户数
    community_num = soup.select(
        '#community > div.community-info > div:nth-child(1) > div.community-info-td.community-info-right > p.community-info-td-value')
    community_num = community_num[0].get_text().strip() if len(community_num) != 0 else ''
    #  print("小区户数：" + community_num.get_text().strip())
    # 物业类型
    property_type = soup.select('#houseInfo > table > tbody > tr:nth-child(1) > td:nth-child(3) > span.houseInfo-main-item-name')
    property_type = property_type[0].get_text() if len(property_type) != 0 else ''
    #  print("物业类型：" + property_type.get_text())
    # 房屋售价（万元）
    selling_price = soup.select('#__layout > div > div.props-main > div.props-body > div.props-right > div.maininfo > div.maininfo-price > '
                                'div:nth-child(1) > div.maininfo-price-wrap > span.maininfo-price-num')
    selling_price = selling_price[0].get_text().strip() if len(selling_price) != 0 else ''
    #  print("房屋售价" + selling_price.get_text().strip())
    # 单价（元/㎡）
    unit_price = soup.select('#__layout > div > div.props-main > div.props-body > div.props-right > div.maininfo > div.maininfo-price > '
                             'div:nth-child(1) > div.maininfo-avgprice > div.maininfo-avgprice-price')
    unit_price = unit_price[0].get_text().strip() if len(unit_price) != 0 else ''

    #  print("单价：" + unit_price.get_text().strip())

    # 使用CSS选择器提取每个div:nth-child中的a标签的href属性
    house_id = soup.find('div', class_='banner-title-code')
    # 房屋编码
    house_id = house_id.text.replace('房屋编码：', '')

    data = {
        '房屋编码': house_id,
        '城市': city,
        '行政区': district,
        '所属区域': region,
        '小区名称': community_name,
        '地址': '',
        '建筑面积（㎡）': area,
        '所在层': outside,
        '总层数': inside,
        '房屋户型': house_type,
        '户型结构': '',
        '房屋结构': '',
        '装修状况': renovation_condition,
        '建筑形式': '',
        '房屋用途': part1,
        '建成年份': part2,
        '房屋朝向': asaga,
        '楼户比例': '',
        '发布时间': released,
        '更新时间': update_time,
        '经纪公司': brokerage_firms,
        '经纪人': broker,
        '房本年限': bomoto_term,
        '产权所属': '',
        '产权类型': property_rights,
        '有无大税': '',
        '房龄': house_age,
        '小区户数': community_num,
        '物业类型': property_type,
        '房屋售价（万元）': selling_price,
        '单价（元 /㎡）': unit_price,
        '链接地址': url,
        '营业执照': license
    }
    a.append(data)
    print(data)

error_data = []


def get_community_html(url, city_name):
    payload = {}
    parsed_url = urlparse(url)
    headers = {
        'Cookie': 'sessid=B8EDC173-F262-AA43-02EF-FF82950E2BD9; aQQ_ajkguid=B937A289-AAD3-C14A-311C-E38CC41A793B; twe=2; ajk-appVersion=; id58=CrIW6mZf7liYqGPjGb93Ag; isp=true; 58tj_uuid=da66cb15-a4f9-4ce6-b201-ed4afc2a4aac; xxzlclientid=c9503abf-1d2c-418c-b736-1717563229691; xxzlxxid=pfmxR+94+OV9CbCo7QUVMJ5AXt+MaBFd0vb76A58s9iZSTZ+fJHZqJMG5UMzPqfh8aXc; als=0; lps=https%3A%2F%2Fheb.zu.anjuke.com%2F%3Ffrom%3DHomePage_TopBar%7Chttps%3A%2F%2Fheb.anjuke.com%2F; cmctid=202; xxzlbbid=pfmbM3wxMDM1MXwxLjguMXwxNzE3NTczMzI2ODkyfG52MmsrQzRxRVd0MDBRUlJqbXl4eGhSMzQzU1poRk1UL2J2UTIyc1B3d3c9fDM1YWNjNWNhYzNhODc5YzA1MGFiNDQ3YjkzYzEzMTE4XzE3MTc1NzMzMzI1ODFfZmJhMGY5NTYzODdhNDAwODk1ZTg4YzQ3ZDlkNzRlZjVfMTAzMTg0ODczM3w3YzUwNWQ2N2E5YTJmMGM1ODk3ZWQ1Yjk3YzQyMzUyY18xNzE3NTczMzI2NDEyXzI1Ng; ajk_member_verify=ZtrRHaydORjVQQetzDoL0XZIcdPlU5pHNf3lLFLu%2BQE%3D; ajk_member_verify2=MjIxMzk0MzI4fG00ZmRFOWp8MQ%3D%3D; ajk_member_id=221394328; _ga=GA1.2.191220906.1717596493; new_uv=5; _ga_DYBJHZFBX2=GS1.2.1717683580.4.0.1717683580.0.0.0; fzq_h=5643a6d45f8670914b51a805ef3818e8_1717849347990_0c0b6c8be6c34b5b9980c3ddd74a1f93_1031848733; ctid=128; obtain_by=2; xxzl_cid=38d85cfe6dec4298be0f4acaa3f6924a; xxzl_deviceid=79zLeHNhROJJUjkSislV8bFzRvMJfksQ5xOYOZKGKJjNWvJlHleqo/irvPnNNzrb; ajkAuthTicket=TT; fzq_js_anjuke_xiaoqu_pc=b869cfca75f455493308e7772d5b971b_1717853899237_24; ctid=205; aQQ_ajkguid=B937A289-AAD3-C14A-311C-E38CC41A793B; obtain_by=2; twe=2; sessid=1CA556AA-0360-4EC5-B7D9-3B9F96C5F5B7; ajk-appVersion=; fzq_h=e04a35c04b5ad936b524b6e516f1c2f7_1717853894654_9158aa5c971e478999fb791e178f7c7c_1031848733; id58=CrIclWZkXsZ5732JXqwFAg==',
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
            href = tag['href']
            print(f'要抓取的链接：{href}')
            retries = 5
            while retries > 0:
                try:
                    get_detail(city_name, href)
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
    df = pd.read_excel('可读城市.xlsx')
    for index, row in df.iterrows():
        # 总条数
        total = row["总数"]
        # 获取的总数
        get_community_total = 0
        print(f'城市：{row["城市"]}，链接：{row["链接"]}，总数{total}')
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
                    community_detail = get_community_html(url, row["城市"])
                    # 每页数据获取
                    print(f'页数：{page_num}，已获取条数{community_detail}')
                    if int(community_detail) == 0:
                        not_data.append(url)
                    get_community_total += community_detail
                    page_num += 1
                    break
                except Exception as e:
                    retries -= 1
                    print(f'获取{row["城市"]}第{page_num}页数据时发生错误。重试中...（剩余重试次数：{retries}）')
                    print(f'异常信息：{e}')

    # info()
    # print(a)
    df_out = pd.DataFrame(a, columns=['房屋编码', '城市', '行政区', '所属区域', '小区名称', '地址', '建筑面积（㎡）', '所在层', '总层数', '房屋户型',
                                      '户型结构', '房屋结构', '装修状况', '建筑形式', '房屋用途', '建成年份', '房屋朝向', '楼户比例', '发布时间',
                                      '更新时间', '经纪公司', '经纪人', '房本年限', '产权所属', '产权类型', '有无大税', '房龄', '小区户数',
                                      '物业类型', '房屋售价（万元）', '单价（元 /㎡）', '链接地址'
                                      ])
    df_out.to_excel('测试数据demo.xlsx')
    print(f'空数据：{not_data}')
    print(f'链接获取错误数据：{error_data}')
