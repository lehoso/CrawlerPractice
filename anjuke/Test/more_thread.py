import http
import re
import time
from urllib.parse import urlparse

import pandas as pd
from concurrent.futures import ThreadPoolExecutor, ProcessPoolExecutor
import numpy as np
from bs4 import BeautifulSoup


# 读取Excel文件并将数据保存在列表中
def read_excel_to_list(file_path):
    df = pd.read_excel(file_path)
    data_list = df.values.tolist()
    return data_list


a = []


def get_detail(city, url):
    print("当前链接：" + url)
    parsed_url = urlparse(url)
    conn = http.client.HTTPSConnection(parsed_url.hostname)
    payload = ''
    headers = {
        'Cookie': 'sessid=EB0916E6-A21A-5924-51B6-45772B5B8B0A; aQQ_ajkguid=F8FDD31B-2A60-B975-04FE-B03671FD72E5; ctid=20; twe=2; ajk-appVersion=; fzq_h=6980d6a48c3f3ae6f2619644413a2a90_1717960823205_e2dab851a6974124b898762a18c11d7c_3085060277; obtain_by=2; id58=CrIgxGZmAHhSb5GsfuWyAg==; xxzl_cid=58f57b88d1fc4127b5577d3a62307b6b; xxzl_deviceid=vIu4rQuMYVIQVXD7pAdg+XZ6hJH3l69CwZPTnzQkBQ4a3tKSIw4dIZx07ev8e1A9',
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
    district = soup.select(
        '#__layout > div > div.props-main > div.props-body > div.props-right > div.maininfo > div.maininfo-meta >'
        ' div.maininfo-community > div:nth-child(2) > span.maininfo-community-item-name > a:nth-child(1)')
    district = district[0].get_text() if len(district) != 0 else ''
    #  print("行政区：" + district.get_text())
    # 所属区域
    region = soup.select(
        '#__layout > div > div.props-main > div.props-body > div.props-right > div.maininfo > div.maininfo-meta >'
        ' div.maininfo-community > div:nth-child(2) > span.maininfo-community-item-name > a:nth-child(2)')
    region = region[0].get_text() if len(region) != 0 else ''

    #  print("所属区域：" + region.get_text())
    # 小区名称
    community_name = soup.select(
        '#__layout > div > div.props-main > div.banner > div.banner-breadCrumbs > div > a:nth-child(5)')
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
    renovation_condition = soup.select(
        '#__layout > div > div.props-main > div.props-body > div.props-right > div.maininfo > div.maininfo-model > '
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
    asaga = soup.select(
        '#__layout > div > div.props-main > div.props-body > div.props-right > div.maininfo > div.maininfo-model > '
        'div.maininfo-model-item.maininfo-model-item-3 > div.maininfo-model-strong > i')
    asaga = asaga[0].get_text() if len(asaga) != 0 else ''

    #  print("房屋朝向：" + asaga.get_text())
    # 楼户比例
    # 发布时间
    released = soup.select(
        '#houseInfo > table > tbody > tr:nth-child(7) > td.houseInfo-main-item-first > span.houseInfo-main-item-name')
    released = released[0].get_text() if len(released) != 0 else ''

    # 营业执照
    license = soup.select(
        'houseInfo > table > tbody > tr:nth-child(6) > td.houseInfo-main-item-first > span.houseInfo-main-item-name')
    license = license[0].get_text() if len(license) != 0 else ''

    #  print("发布时间：" + released.get_text())
    # 更新时间
    update_time = soup.select(
        '#houseInfo > table > tbody > tr:nth-child(7) > td.houseInfo-main-item-first > span.houseInfo-main-item-name')
    update_time = update_time[0].get_text() if len(update_time) != 0 else ''

    #  print("更新时间：" + update_time.get_text())
    # 经纪公司
    brokerage_firms = soup.select(
        '#__layout > div > div.props-main > div.props-body > div.props-right > div.maininfo > div.maininfo-broker > div.maininfo-broker-info > div.maininfo-broker-info-company > div > a')
    brokerage_firms = brokerage_firms[0].get_text().strip() if len(brokerage_firms) != 0 else ''
    #  print("经纪公司：" + brokerage_firms.get_text())
    # 经纪人
    broker = soup.select(
        '#__layout > div > div.props-main > div.props-body > div.props-right > div.maininfo > div.maininfo-broker > '
        'div.maininfo-broker-info > div.maininfo-broker-info-title > div.maininfo-broker-info-name')
    broker = broker[0].get_text() if len(broker) != 0 else ''
    #  print("经纪人" + broker.get_text())
    # 房本年限
    bomoto_term = soup.select(
        '#houseInfo > table > tbody > tr:nth-child(2) > td.houseInfo-main-item-first > span.houseInfo-main-item-name')
    bomoto_term = bomoto_term[0].get_text() if len(bomoto_term) != 0 else ''

    #  print("房本年限:" + bomoto_term.get_text())
    # 产权所属

    # 产权类型
    property_rights = soup.select(
        '#houseInfo > table > tbody > tr:nth-child(1) > td.houseInfo-main-item-first > span.houseInfo-main-item-name')
    property_rights = property_rights[0].get_text() if len(property_rights) != 0 else ''

    #  print("产权所属：" + property_rights.get_text())
    # 有无大税
    # 房龄
    house_age = soup.select(
        '#houseInfo > table > tbody > tr:nth-child(2) > td:nth-child(3) > span.houseInfo-main-item-name')
    house_age = house_age[0].get_text() if len(house_age) != 0 else None

    #  print("房龄：" + house_age.get_text())
    # 小区户数
    community_num = soup.select(
        '#community > div.community-info > div:nth-child(1) > div.community-info-td.community-info-right > p.community-info-td-value')
    community_num = community_num[0].get_text().strip() if len(community_num) != 0 else ''
    #  print("小区户数：" + community_num.get_text().strip())
    # 物业类型
    property_type = soup.select(
        '#houseInfo > table > tbody > tr:nth-child(1) > td:nth-child(3) > span.houseInfo-main-item-name')
    property_type = property_type[0].get_text() if len(property_type) != 0 else ''
    #  print("物业类型：" + property_type.get_text())
    # 房屋售价（万元）
    selling_price = soup.select(
        '#__layout > div > div.props-main > div.props-body > div.props-right > div.maininfo > div.maininfo-price > '
        'div:nth-child(1) > div.maininfo-price-wrap > span.maininfo-price-num')
    selling_price = selling_price[0].get_text().strip() if len(selling_price) != 0 else ''
    #  print("房屋售价" + selling_price.get_text().strip())
    # 单价（元/㎡）
    unit_price = soup.select(
        '#__layout > div > div.props-main > div.props-body > div.props-right > div.maininfo > div.maininfo-price > '
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


error_data_link = []


# 定义处理每条数据的函数
def process_data(data):
    # 城市
    # 小区
    # 链接
    # 打印每条数据
    print(f'城市：{data[1]},小区名：{data[2]}，：链接{data[3]}')
    # 解析URL
    parsed_url = urlparse(data[3])
    # 提取路径中的特定部分
    path = parsed_url.path
    match = re.search(r'/prop/view/([^/]+)', path)
    # 重新构造所需的URL部分
    base_url = f"{parsed_url.scheme}://{parsed_url.netloc}{parsed_url.path}"
    if match:
        property_id = match.group(1)
        print("保留的ID部分:", property_id)
    else:
        print("未找到匹配的ID部分")
    retries = 3
    while retries > 0:
        try:
            get_detail(data[1], base_url)
            break
        except Exception as e:
            retries -= 1
            print(f'城市：{data[1]},链接：{data[2]}，小区名：{data[3]},剩余重试次数：{retries}')
            # 错误连接
            if retries == 0:
                error_data_link.append(data[2])
                break
            print(f'异常信息：{e}')


# 使用线程池进行多线程处理每个数据块
def process_block_with_threads(data_block, thread_workers=2):  # 使用6个线程
    with ThreadPoolExecutor(max_workers=thread_workers) as executor:
        executor.map(process_data, data_block)


# 使用进程池进行多进程处理，将数据列表分块并在每个进程中使用多线程处理
def process_with_processes_and_threads(data_list, process_workers=2, thread_workers=2):  # 使用6个进程和6个线程
    # 分块数据列表
    data_blocks = np.array_split(data_list, process_workers)
    with ProcessPoolExecutor(max_workers=process_workers) as executor:
        for data_block in data_blocks:
            executor.submit(process_block_with_threads, data_block, thread_workers)


# 主函数
if __name__ == "__main__":
    # 城市
    # 小区
    # 链接

    file_path = '小区二手房大于100的小区part1.xlsx'

    # 将Excel文件中的数据读取到列表中
    data_list = read_excel_to_list(file_path)
    # for data in data_list:
    #     process_data(data)

    # 使用多进程和多线程处理数据
    process_with_processes_and_threads(data_list)
    df_out = pd.DataFrame(a, columns=['房屋编码', '城市', '行政区', '所属区域', '小区名称', '地址', '建筑面积（㎡）',
                                      '所在层', '总层数', '房屋户型',
                                      '户型结构', '房屋结构', '装修状况', '建筑形式', '房屋用途', '建成年份',
                                      '房屋朝向', '楼户比例', '发布时间',
                                      '更新时间', '经纪公司', '经纪人', '房本年限', '产权所属', '产权类型', '有无大税',
                                      '房龄', '小区户数',
                                      '物业类型', '房屋售价（万元）', '单价（元 /㎡）', '链接地址'
                                      ])
    df_out.to_excel('详细数据.xlsx')
    print(f'链接获取错误数据：{error_data_link}')