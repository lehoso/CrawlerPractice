import requests

url = 'http://www.baidu.com'

proxies = {
    'http': 'http://222.74.237.246:808',
    'https': 'https://222.74.237.246:808',
}
try:
    response = requests.get(url, proxies=proxies, timeout=10)
    if response.status_code == 200:
        if '百度一下' in response.text:
            print('代理IP可用：', proxies)
        else:
            print('代理IP不可用：', proxies)
    else:
        print('代理IP不可用：', proxies)
except:
    print('代理IP不可用：', proxies)
