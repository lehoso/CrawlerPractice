import http.client
import re
from urllib.parse import urlparse
from bs4 import BeautifulSoup
import pandas as pd
import requests
import json
import time
from queue import Queue
from threading import Thread, Lock
from concurrent.futures import ProcessPoolExecutor, as_completed

# 全局变量
a = []
error_data_link = []


def get_detail(city, url, proxy):
    parsed_url = urlparse(url)
    headers = {
        'User-Agent': 'Apifox/1.0.0 (https://apifox.com)',
        'Accept': '*/*',
        'Host': parsed_url.hostname,
        'Connection': 'keep-alive'
    }

    conn = http.client.HTTPSConnection(parsed_url.hostname)
    # conn = http.client.HTTPSConnection(proxy)
    # conn.set_tunnel(parsed_url.hostname)  # 设置隧道连接到目标主机
    conn.request("GET", url, headers=headers)
    res = conn.getresponse()
    data = res.read()
    html_content = data.decode("utf-8")
    soup = BeautifulSoup(html_content, 'lxml')

    # 提取数据
    district = soup.select_one('#__layout .maininfo-community-item-name a:nth-child(1)')
    district = district.get_text() if district else ''

    region = soup.select_one('#__layout .maininfo-community-item-name a:nth-child(2)')
    region = region.get_text() if region else ''

    community_name = soup.select_one('#__layout .banner-breadCrumbs a:nth-child(5)')
    community_name = community_name.get_text() if community_name else ''

    area = (soup.find('div', class_='maininfo-model-item maininfo-model-item-2')
            .find('div', class_='maininfo-model-strong')
            .find('i', class_='maininfo-model-strong-num'))
    area = area.text if area else ''

    floors = soup.find('div', class_='maininfo-model-weak')
    floors = floors.text if floors else ''
    match = re.match(r'([^()]+)\(([^()]+)\)', floors)
    if match:
        outside, inside = match.groups()
    else:
        outside = floors
        inside = ''

    house_type = soup.find('div', class_='maininfo-model-strong')
    house_type = house_type.text if house_type else ''

    renovation_condition = (soup.find('div', class_='maininfo-model-item maininfo-model-item-2')
                            .find('i', class_='maininfo-model-weak'))
    renovation_condition = renovation_condition.text if renovation_condition else ''

    purpose_year = soup.select_one('#__layout .maininfo-model-item-3 .maininfo-model-weak')
    purpose_year = purpose_year.get_text() if purpose_year else ''
    parts = purpose_year.split('/')
    part1 = parts[0] if len(parts) > 0 else ''
    part2 = parts[1] if len(parts) > 1 else ''

    asaga = soup.select_one('#__layout .maininfo-model-item-3 .maininfo-model-strong i')
    asaga = asaga.get_text() if asaga else ''

    released = soup.select_one('#houseInfo tr:nth-child(7) span.houseInfo-main-item-name')
    released = released.get_text() if released else ''

    update_time = soup.select_one('#houseInfo tr:nth-child(7) span.houseInfo-main-item-name')
    update_time = update_time.get_text() if update_time else ''

    brokerage_firms = soup.select_one('#__layout .maininfo-broker-info-company a')
    brokerage_firms = brokerage_firms.get_text().strip() if brokerage_firms else ''

    broker = soup.select_one('#__layout .maininfo-broker-info-name')
    broker = broker.get_text() if broker else ''

    bomoto_term = soup.select_one('#houseInfo tr:nth-child(2) span.houseInfo-main-item-name')
    bomoto_term = bomoto_term.get_text() if bomoto_term else ''

    property_rights = soup.select_one('#houseInfo tr:nth-child(1) span.houseInfo-main-item-name')
    property_rights = property_rights.get_text() if property_rights else ''

    house_age = soup.select_one('#houseInfo tr:nth-child(2) span:nth-child(3)')
    house_age = house_age.get_text() if house_age else ''

    community_num = soup.select_one('#community .community-info-td-value')
    community_num = community_num.get_text().strip() if community_num else ''

    property_type = soup.select_one('#houseInfo tr:nth-child(1) span:nth-child(3)')
    property_type = property_type.get_text() if property_type else ''

    selling_price = soup.select_one('#__layout .maininfo-price-num')
    selling_price = selling_price.get_text().strip() if selling_price else ''

    unit_price = soup.select_one('#__layout .maininfo-avgprice-price')
    unit_price = unit_price.get_text().strip() if unit_price else ''

    house_id = soup.find('div', class_='banner-title-code')
    house_id = house_id.text.replace('房屋编码：', '') if house_id else ''

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
        '房屋用途': part2,
        '建成年份': part1,
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
        '营业执照': ''
    }
    a.append(data)
    print(data)


def read_excel_to_list(file_path):
    df = pd.read_excel(file_path)
    return df.values.tolist()


def get_proxy():
    url = "http://www.zdopen.com/ShortProxy/GetIP/?api=202406101241266168&akey=4423016021e29721&count=5&timespan=1&type=3"
    headers = {
        'User-Agent': 'Apifox/1.0.0 (https://apifox.com)',
        'Accept': '*/*',
        'Host': 'www.zdopen.com',
        'Connection': 'keep-alive'
    }
    response = requests.get(url, headers=headers)
    response_data = response.json()
    proxies = response_data['data']['proxy_list']
    proxy_pool = [f"{proxy['ip']}:{proxy['port']}" for proxy in proxies]
    return proxy_pool


def proxy_updater(proxy_queue, lock):
    while True:
        new_proxies = get_proxy()
        with lock:
            while not proxy_queue.empty():
                proxy_queue.get()
            for proxy in new_proxies:
                proxy_queue.put(proxy)
        time.sleep(10)


def process_data(data, proxy):
    try:
        get_detail(data[0], data[2], proxy)
    except Exception as error:
        error_data_link.append(data)


def main(file_path):
    data_list = read_excel_to_list(file_path)

    proxy_queue = Queue()
    lock = Lock()

    # 启动一个线程定期更新代理池
    updater_thread = Thread(target=proxy_updater, args=(proxy_queue, lock))
    updater_thread.daemon = True
    updater_thread.start()

    with ProcessPoolExecutor() as process_executor:
        futures = []
        for i in range(0, len(data_list), 15):
            split_data = data_list[i:i + 15]

            for j in range(0, len(split_data), 3):
                data_batch = split_data[j:j + 3]

                for data in data_batch:
                    with lock:
                        if proxy_queue.empty():
                            proxy = None
                        else:
                            proxy = proxy_queue.get()
                            proxy_queue.put(proxy)  # 将代理重新放回队列
                    futures.append(process_executor.submit(process_data, data, proxy))

        for future in as_completed(futures):
            try:
                future.result()
            except Exception as exc:
                print(f'产生了一个异常: {exc}')


# 主函数
if __name__ == "__main__":
    url = 'https://daqing.anjuke.com/prop/view/R3560258284250122?auction=201&hpType=1&entry=136&position=25&kwtype=comm_one&now_time=1717939798&spread=commsearch_p&from=PC_COMM_ESF_LIST_CLICK&index=25'
    get_detail('x', url, '117.28.40.106:42122')
    # file_path = '小区二手房大于100的小区1_3.xlsx'
    # main(file_path)
    #
    # df_out = pd.DataFrame(a, columns=['房屋编码', '城市', '行政区', '所属区域', '小区名称', '地址', '建筑面积（㎡）',
    #                                   '所在层', '总层数', '房屋户型',
    #                                   '户型结构', '房屋结构', '装修状况', '建筑形式', '房屋用途', '建成年份',
    #                                   '房屋朝向', '楼户比例', '发布时间',
    #                                   '更新时间', '经纪公司', '经纪人', '房本年限', '产权所属', '产权类型', '有无大税',
    #                                   '房龄', '小区户数',
    #                                   '物业类型', '房屋售价（万元）', '单价（元 /㎡）', '链接地址'
    #                                   ])
    # df_out.to_excel('详细数据.xlsx')
    # print(f'链接获取错误数据：{len(error_data_link)}')
    # df_out_error = pd.DataFrame(error_data_link, columns=['城市', '小区', '链接'])
    # df_out_error.to_excel('异常数据.xlsx')
