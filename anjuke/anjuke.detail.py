import http.client
import re
import time

import pandas as pd
from bs4 import BeautifulSoup

'''
详细链接
'''

a = []


def get_detail(city, url):
    print("当前链接：" + url)
    conn = http.client.HTTPSConnection("heb.anjuke.com")
    payload = ''
    headers = {
        'Cookie': 'xxzlxxid=pfmxR+94+OV9CbCo7QUVMJ5AXt+MaBFd0vb76A58s9iZSTZ+fJHZqJMG5UMzPqfh8aXc',
        'User-Agent': 'Apifox/1.0.0 (https://apifox.com)',
        'Accept': '*/*',
        'Host': 'heb.anjuke.com',
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
    if match:
        outside, inside = match.groups()
        # 所在层
    #  print("楼层等级:", outside)
    # 总层数
    #  print("总共层数:", inside)
    else:
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


def info():
    conn = http.client.HTTPSConnection("heb.anjuke.com")
    payload = ''
    headers = {
        'Cookie': 'Cookie=aQQ_ajkguid=91B5999B-22B8-4250-B6CD-415A201678F4; sessid=B3C5073A-2F0C-4920-8D86-6580E617F88E; ajk-appVersion=; ctid=48; fzq_h=053b1eee8d9988868436ada9d14bd4c2_1717571528615_626e4d04f9164ef296613f29c237103a_1031848733; obtain_by=2; twe=2; id58=CroD4GZgD8hGvowwHTQ8Ag==; xxzlclientid=e6c5cb6b-9400-4627-8b46-1717571523594; xxzlxxid=pfmxR+94+OV9CbCo7QUVMJ5AXt+MaBFd0vb76A58s9iZSTYCa50BAHB8ayLEi7F5KJtz; xxzlbbid=pfmbM3wxMDM1MXwxLjguMHwxNzE3NTcxNTI0NTYxfDlYY29qZjZYUmhCTVZ6L21ZMHhtWTBtRmNKZkJMekQxbzFzUkhrNEpaZDA9fGEyYjk5NWVkOTExYWIwMjA2MDExYzA3NDFlZjFiMDMxXzE3MTc1NzE1Mjk2MDNfYzRhNTdhNzNkNzc0NDYwZWI0OWI0NDZjMGZiN2U0MzdfMTAzMTg0ODczM3xjYzEzZjk2MTQ2MzZlYzc0ZmZmYzgyN2Q2MTE3YTFjMV8xNzE3NTcxNTIzNDY3XzI1NA==; ajk_member_verify=ZtrRHaydORjVQQetzDoL0XZIcdPlU5pHNf3lLFLu%2BQE%3D; ajk_member_verify2=MjIxMzk0MzI4fG00ZmRFOWp8MQ%3D%3D; 58tj_uuid=047cd729-23b4-42d7-acf7-0bc41f85b9dc; new_session=1; init_refer=https%253A%252F%252Fheb.anjuke.com%252F; new_uv=1; _ga=GA1.2.1311648480.1717571551; _gid=GA1.2.900944922.1717571551; _gat=1; _ga_DYBJHZFBX2=GS1.2.1717571551.1.0.1717571551.0.0.0; als=0; fzq_js_anjuke_ershoufang_pc=a34fe04c32582f523a2c692f74bffc79_1717571555132_25; ajk_member_id=221394328; xxzl_cid=bc86a498670945cc8d3878d8e68c5afb; xxzl_deviceid=AN1gYk3DOg7Cp1YT1lVGWtA/GzNOh0xDybmXAyGsDCqYo3/D+ynyNRilOPFTN0zM; ajkAuthTicket=TT=2f996fae8456da4c9ff0e2e228bed376&TS=1717571572431&PBODY=WX8EhF7jmPt0p-BIwm0okq9-nDKMSYzo33_ZOhTUFM9HC0xnxM18xQ7QWY9Ch3t-xqCd9rEnVLiT4uChg6_BzF-uf9J0njGI9synWb_EdWMrqaWOdFk4xnja66RwsZO5DbVVPpsIcDN8pNjrK_MXcUjVOn2_8zKYmzAqJDo38cg&VER=2&CUID=4eGSxIUoYdqQQOls3Krf9aS2r3T3qS61; fzq_js_anjuke_xiaoqu_pc=046406a3e06dcb6a6db0b0b827809fcd_1717571566779_24; aQQ_ajkguid=8E0AA674-C7C3-4D92-B008-FE8F310A6559; sessid=1037C4F8-0443-4F52-BB83-5A596414FEC9; ajk-appVersion=; ctid=48; fzq_h=d16b54e375f842d6cd02e3fe08661213_1717564406398_3c4044d7a053401289bf461b8862961b_1031848733; obtain_by=2; twe=2; id58=CrIej2ZgENJZX815HXzuAg==; ajkAuthTicket=TT=2f996fae8456da4c9ff0e2e228bed376&TS=1717571820293&PBODY=DOcGGTBbJRmhb2LmcKcFueQsRSov146pAfprKTaNOKfvx5XGjnZnVIwthONcYGq2-ET0pRqqUyoktNert_NB-6NY4Wy74csW0xQ_E4VicgpV8Dysl-_MDRfFkfFaPLX4fEyWhygZiTme-gYmSUMb0FNNSERB50uDpBeobaz_WDw&VER=2&CUID=4eGSxIUoYdqQQOls3Krf9aS2r3T3qS61',
        'User-Agent': 'Apifox/1.0.0 (https://apifox.com)',
        'Accept': '*/*',
        'Host': 'heb.anjuke.com',
        'Connection': 'keep-alive'
    }
    conn.request("GET", "/community/props/sale/355338", payload, headers)
    res = conn.getresponse()
    data = res.read()
    # 将HTML内容保存为data.html文件
    html_content = data.decode("utf-8")
    # with open("355338.html", "w", encoding="utf-8") as file:
    #     file.write(html_content)
    #
    # # 使用BeautifulSoup解析保存的HTML文件
    # with open("355338.html", "r", encoding="utf-8") as file:
    #     soup = BeautifulSoup(file, 'lxml')
    soup = BeautifulSoup(html_content, 'lxml')

    # 使用CSS选择器提取每个div:nth-child中的a标签的href属性
    selector = "#__layout > div > section > section.list-main > section > section:nth-child(2) > div:nth-child(n) > a"
    tags = soup.select(selector)

    # 输出每个匹配的a标签的href属性
    for tag in tags:
        if tag and 'href' in tag.attrs:
            href = tag['href']
            get_detail('哈尔滨', href)
            # print(href)
            time.sleep(5)
        else:
            print("未找到标签或标签不包含href属性。")


if __name__ == '__main__':
    # url = 'https://heb.anjuke.com/prop/view/S2754299020782597?auction=221&hpType=27&entry=136&position=20&kwtype=comm_one&now_time=1717596519&spread=commsearch_c&epauction=&stats_key=f1448ac6-7fbd-4b2f-9a8b-fb6b449ddba2_20&from=PC_COMM_ESF_LIST_CLICK&index=20'
    # get_detail('哈尔滨', url)
    info()
    # print(a)
    df_out = pd.DataFrame(a, columns=['房屋编码',
                                      '城市',
                                      '行政区',
                                      '所属区域',
                                      '小区名称',
                                      '地址',
                                      '建筑面积（㎡）',
                                      '所在层',
                                      '总层数',
                                      '房屋户型',
                                      '户型结构',
                                      '房屋结构',
                                      '装修状况',
                                      '建筑形式',
                                      '房屋用途',
                                      '建成年份',
                                      '房屋朝向',
                                      '楼户比例',
                                      '发布时间',
                                      '更新时间',
                                      '经纪公司',
                                      '经纪人',
                                      '房本年限',
                                      '产权所属',
                                      '产权类型',
                                      '有无大税',
                                      '房龄',
                                      '小区户数',
                                      '物业类型',
                                      '房屋售价（万元）',
                                      '单价（元 /㎡）',
                                      '链接地址'
                                      ])
    df_out.to_excel('测试数据demo.xlsx')
