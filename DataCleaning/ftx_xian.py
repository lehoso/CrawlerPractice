import pandas as pd
import numpy as np
import pymysql

pymysql.install_as_MySQLdb()
from sqlalchemy import create_engine

df = pd.read_csv(r'ftx_xian3.csv', encoding='utf-8')
# print(len(df))
# 1.去重复值
df_clean = df.drop_duplicates(subset='title', keep='first')  # 主键 关键字段，删除
# print(len(df_clean))

# 2去空值
df_clean = df_clean.dropna()  # 1.删除，2替换，3插值
# 3
df_clean = df_clean.reset_index()  # 重置索引号
# print(df_clean)
for j in range(len(df_clean)):  # 循环访问每一行数据
    if (float(df_clean.iloc[j, 7]) > 2021):
        df_clean.iloc[j, 7] = 2013  # 中位数替代
    if (float(df_clean.iloc[j, 16]) < 0):# 如果有负数
        df_clean.iloc[j, 16] = abs(float(df_clean.iloc[j, 16]))  #取绝对值
# print(len(df_clean))

df_clean = df_clean[['title', 'housetype', 'floor', 'orientation',
                     'yearbuilt', 'Street', 'area', 'unitprice']]
df_clean = df_clean[1:10]
print(df_clean)
# print(len(df_clean))

out = pd.DataFrame(df_clean,
                   columns=['title', 'housetype', 'floor', 'orientation',
                            'yearbuilt', 'Street', 'area', 'unitprice'],
                   )
#存一份csv查看
out.to_csv('test3.csv')
#数据库连接
# conn = create_engine('mysql+mysqldb://root:000000@localhost:3306/keshihua?charset=utf8')
# out.to_sql(name='ershoufang2',con=conn,if_exists='append',index=False,index_label=False)
