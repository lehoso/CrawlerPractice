import http.client
import json
import random
import re
from urllib.parse import urlparse

import requests
from bs4 import BeautifulSoup


# 获取代理池
def get_proxy():
    url = "http://www.zdopen.com/ShortProxy/GetIP/?api=202406101241266168&akey=4423016021e29721&count=5&timespan=3&type=3"
    payload = {}
    headers = {
        'User-Agent': 'Apifox/1.0.0 (https://apifox.com)',
        'Accept': '*/*',
        'Host': 'www.zdopen.com',
        'Connection': 'keep-alive'
    }
    response = requests.request("GET", url, headers=headers, data=payload)
    response_data = json.loads(response.text)
    proxies = response_data['data']['proxy_list']
    proxy_pool = [f"{proxy['ip']}:{proxy['port']}" for proxy in proxies]
    return proxy_pool


def get_random_proxy():
    # 获取代理池
    proxy_pool = get_proxy()
    return random.choice(proxy_pool)


def get_test():
    import http.client
    proxy = get_random_proxy()
    conn = http.client.HTTPSConnection(proxy)
    payload = ''
    headers = {
        'User-Agent': 'Apifox/1.0.0 (https://apifox.com)',
        'Accept': '*/*',
        'Host': 'www.baidu.com',
        'Connection': 'keep-alive'
    }
    conn.set_tunnel("www.baidu.com")  # 设置隧道连接到目标主机
    conn.request("GET", "/", payload, headers)
    res = conn.getresponse()
    data = res.read()
    print(data.decode("utf-8"))


a = []
if __name__ == '__main__':
    get_test()
