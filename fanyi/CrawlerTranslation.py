# -*- coding: utf-8 -*-
# @Author  : LEHOSO
# @FileName: CrawlerTranslation.py
# @Time    : 2021/9/28 00:06
import hashlib
import json
import random
import time

import requests


class Transaction(object):

    def __init__(self, words):
        self.url = "https://fanyi.youdao.com/translate_o?smartresult=dict&smartresult=rule"
        # 固定的字符串，也许定期更新，建议使用前先看fanyi.min.js中值
        self.D = "Y2FYu%TNSbMCxc3t2u^XT"
        self.words = words
        '''
        headers里面有一些参数是必须的，注释掉的可以不用带上
        '''
        self.headers = {
            # cookie记得更换，User-Agent建议使用自己的
            'Cookie': 'OUTFOX_SEARCH_USER_ID=-1116370259@10.108.160.105; OUTFOX_SEARCH_USER_ID_NCOO=1270485896.3705344; _ntes_nnid=95952ff489382b5b3c9bae441741a0cc,1624695942786; _ga=GA1.2.1254647712.1630264192; hb_MA-BFF5-63705950A31C_source=cn.bing.com; mp_MA-BFF5-63705950A31C_hubble=%7B%22sessionReferrer%22%3A%20%22https%3A%2F%2Fke.study.youdao.com%2Fcourse%2Fdetail%2F100082196%22%2C%22updatedTime%22%3A%201632195450694%2C%22sessionStartTime%22%3A%201632195449523%2C%22sendNumClass%22%3A%20%7B%22allNum%22%3A%202%2C%22errSendNum%22%3A%200%7D%2C%22deviceUdid%22%3A%20%22fe67124e-f072-4682-912e-ed7707003a97%22%2C%22persistedTime%22%3A%201632195449519%2C%22LASTEVENT%22%3A%20%7B%22eventId%22%3A%20%22c3081d0b687c67f10f51e4d0c980bf15a5c5ce8f%22%2C%22time%22%3A%201632195450694%7D%2C%22sessionUuid%22%3A%20%22aa02107a-abfc-4675-b224-da9c4f87c042%22%7D',
            'Referer': 'http://fanyi.youdao.com/',
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.131 Safari/537.36"
        }
        self.salt = self.get_salt()
        self.sign = self.get_sign()
        '''
        post里面有一些参数是必须的，注释掉的可以不用带上
        如果没有结果出现，则把注释掉的重新启用
        '''
        self.post_data = {
            "i": self.words,
            "from": "AUTO",
            "to": "AUTO",
            # 'smartresult': 'dict',
            'client': 'fanyideskweb',
            'salt': self.salt,
            'sign': self.sign,
            # 'doctype': 'json',
            'version': '2.1',
            'keyfrom': 'fanyi.web',
            # 'action': 'FY_BY_CL1CKBUTTON',
            'typoResult': 'true'
        }

    def get_md(self, value):
        '''md5加密'''
        m = hashlib.md5()
        m.update(value.encode('utf-8'))
        return m.hexdigest()

    def get_salt(self):
        '''
        根据当前时间戳获取salt参数
        '''
        s = int(time.time() * 1000) + random.randint(0, 10)
        return str(s)

    def get_sign(self):
        '''
        使用md5函数和其他参数，得到sign参数
        '''
        s = "fanyideskweb" + self.words + self.salt + self.D
        return self.get_md(s)

    def get_data(self):
        response = requests.post(self.url, headers=self.headers, data=self.post_data)
        # 默认返回bytes类型，除非确定外部调用使用str才进行解码操作
        return response.content

    def parse_data(self, data):

        # 将json数据转换成python字典
        dict_data = json.loads(data)

        # 从字典中抽取翻译结果
        try:
            print(dict_data['translateResult'][0][0]['tgt'])
        except:
            pass

    def run(self):
        """
        url
        headers
        post——data
        发送请求
        :return:
        """

        data = self.get_data()
        # print(data)
        # 解析
        self.parse_data(data)


if __name__ == '__main__':
    Transaction = Transaction(input("请输入要翻译的内容："))
    Transaction.run()

'''
网易翻译反爬机制参考
https://tendcode.com/article/youdao-spider/
'''
