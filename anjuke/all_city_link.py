"""
获取所有城市域名
"""
import http.client

from bs4 import BeautifulSoup
from urllib.parse import urlparse

# anshan.anjuke.com/community/p3/
conn = http.client.HTTPSConnection("anshan.anjuke.com")
payload = ''
headers = {
    'Cookie': 'Cookie=aQQ_ajkguid=91B5999B-22B8-4250-B6CD-415A201678F4; sessid=B3C5073A-2F0C-4920-8D86-6580E617F88E; ajk-appVersion=; ctid=48; fzq_h=053b1eee8d9988868436ada9d14bd4c2_1717571528615_626e4d04f9164ef296613f29c237103a_1031848733; obtain_by=2; twe=2; id58=CroD4GZgD8hGvowwHTQ8Ag==; xxzlclientid=e6c5cb6b-9400-4627-8b46-1717571523594; xxzlxxid=pfmxR+94+OV9CbCo7QUVMJ5AXt+MaBFd0vb76A58s9iZSTYCa50BAHB8ayLEi7F5KJtz; xxzlbbid=pfmbM3wxMDM1MXwxLjguMHwxNzE3NTcxNTI0NTYxfDlYY29qZjZYUmhCTVZ6L21ZMHhtWTBtRmNKZkJMekQxbzFzUkhrNEpaZDA9fGEyYjk5NWVkOTExYWIwMjA2MDExYzA3NDFlZjFiMDMxXzE3MTc1NzE1Mjk2MDNfYzRhNTdhNzNkNzc0NDYwZWI0OWI0NDZjMGZiN2U0MzdfMTAzMTg0ODczM3xjYzEzZjk2MTQ2MzZlYzc0ZmZmYzgyN2Q2MTE3YTFjMV8xNzE3NTcxNTIzNDY3XzI1NA==; ajk_member_verify=ZtrRHaydORjVQQetzDoL0XZIcdPlU5pHNf3lLFLu%2BQE%3D; ajk_member_verify2=MjIxMzk0MzI4fG00ZmRFOWp8MQ%3D%3D; 58tj_uuid=047cd729-23b4-42d7-acf7-0bc41f85b9dc; new_session=1; init_refer=https%253A%252F%252Fheb.anjuke.com%252F; new_uv=1; _ga=GA1.2.1311648480.1717571551; _gid=GA1.2.900944922.1717571551; _gat=1; _ga_DYBJHZFBX2=GS1.2.1717571551.1.0.1717571551.0.0.0; als=0; fzq_js_anjuke_ershoufang_pc=a34fe04c32582f523a2c692f74bffc79_1717571555132_25; ajk_member_id=221394328; xxzl_cid=bc86a498670945cc8d3878d8e68c5afb; xxzl_deviceid=AN1gYk3DOg7Cp1YT1lVGWtA/GzNOh0xDybmXAyGsDCqYo3/D+ynyNRilOPFTN0zM; ajkAuthTicket=TT=2f996fae8456da4c9ff0e2e228bed376&TS=1717571572431&PBODY=WX8EhF7jmPt0p-BIwm0okq9-nDKMSYzo33_ZOhTUFM9HC0xnxM18xQ7QWY9Ch3t-xqCd9rEnVLiT4uChg6_BzF-uf9J0njGI9synWb_EdWMrqaWOdFk4xnja66RwsZO5DbVVPpsIcDN8pNjrK_MXcUjVOn2_8zKYmzAqJDo38cg&VER=2&CUID=4eGSxIUoYdqQQOls3Krf9aS2r3T3qS61; fzq_js_anjuke_xiaoqu_pc=046406a3e06dcb6a6db0b0b827809fcd_1717571566779_24; aQQ_ajkguid=8E0AA674-C7C3-4D92-B008-FE8F310A6559; sessid=1037C4F8-0443-4F52-BB83-5A596414FEC9; ajk-appVersion=; ctid=48; fzq_h=d16b54e375f842d6cd02e3fe08661213_1717564406398_3c4044d7a053401289bf461b8862961b_1031848733; obtain_by=2; twe=2; id58=CrIej2ZgENJZX815HXzuAg==; ajkAuthTicket=TT=2f996fae8456da4c9ff0e2e228bed376&TS=1717571820293&PBODY=DOcGGTBbJRmhb2LmcKcFueQsRSov146pAfprKTaNOKfvx5XGjnZnVIwthONcYGq2-ET0pRqqUyoktNert_NB-6NY4Wy74csW0xQ_E4VicgpV8Dysl-_MDRfFkfFaPLX4fEyWhygZiTme-gYmSUMb0FNNSERB50uDpBeobaz_WDw&VER=2&CUID=4eGSxIUoYdqQQOls3Krf9aS2r3T3qS61',
    'User-Agent': 'Apifox/1.0.0 (https://apifox.com)',
    'Accept': '*/*',
    'Host': 'heb.anjuke.com',
    'Connection': 'keep-alive'
}
conn.request("GET", "/community", payload, headers)
res = conn.getresponse()
data = res.read()
# 将HTML内容保存为data.html文件
html_content = data.decode("utf-8")
with open("355338.html", "w", encoding="utf-8") as file:
    file.write(html_content)

# 使用BeautifulSoup解析保存的HTML文件
with open("anshan.html", "r", encoding="utf-8") as file:
    soup = BeautifulSoup(file, 'html.parser')

# 使用BeautifulSoup解析HTML内容
# 查找所有class为ajk-city-cell-content的ul标签
ul_tags = soup.find_all('ul', class_='ajk-city-cell-content')

# 遍历每个ul标签
for ul in ul_tags:
    # 查找ul标签下的所有li标签
    li_tags = ul.find_all('li')

    # 遍历每个li标签
    for li in li_tags:
        # 查找li标签下的a标签
        a_tag = li.find('a')

        # 获取a标签的href属性和文本内容
        if a_tag:
            href = a_tag.get('href')
            text = a_tag.text
            # 使用urlparse解析URL
            parsed_url = urlparse(href)
            # 获取域名
            domain = parsed_url.netloc
            print(f'href: {href}, domain:{domain}, text: {text}')
