import pandas  # 导入数据统计模块
import matplotlib  # 导入图表模块
import matplotlib.pyplot as plt  # 导入绘图模块

# 避免中文乱码
matplotlib.rcParams['font.sans-serif'] = ['SimHei']  # 设置字体为SimHei显示中文
matplotlib.rcParams['axes.unicode_minus'] = False  # 设置正常显示字符，使用rc配置文件来自定义图形的各种默认属性

# 数据简单清洗
data = pandas.read_csv('data.csv')  # 读取csv数据文件
del data['Unnamed: 0']  # 将索引列删除
data.dropna(axis=0, how='any', inplace=True)  # 删除data数据中的所有空值
data['单价'] = data['单价'].map(lambda d: d.replace('元/平米', ''))  # 将单价“元/平米”去掉
data['单价'] = data['单价'].astype(float)  # 将房子单价转换为浮点类型
data['总价'] = data['总价'].map(lambda z: z.replace('万', ''))  # 将总价“万”去掉
data['总价'] = data['总价'].astype(float)  # 将房子总价转换为浮点类型

data['建筑面积'] = data['建筑面积'].map(lambda p: p.replace('平米', ''))  # 将建筑面价“平米”去掉
data['建筑面积'] = data['建筑面积'].astype(float)  # 将建筑面积转换为浮点类型


# 获取各区二手房均价分析，根据需求，进一步处理数据，如果要写相应算法，需要根据算法所需要的数据来进一步处理数据
def get_average_price():
    group = data.groupby('区域')  # 将房子区域分组   先分组，再切片
    average_price_group = group.size()  # 计算每个区域的均价,average_price_group字典  group['单价'].count()
    x = average_price_group.index  # 区域
    y = average_price_group.values  # 区域对应的均价
    return x, y  # 返回区域与对应的均价,region 二关   average_price均价


# 显示均价条形图
def average_price_bar(x, y, title):
    plt.figure()  # 图形画布
    plt.pie(y, labels=x, labeldistance=1.1,
            autopct="%1.1f%%", shadow=True, startangle=90, pctdistance=0.7)
    plt.axis("equal")  # 设置横轴和纵轴大小相等，这样饼才是圆的
    plt.title(title, fontsize=24)
    plt.legend(bbox_to_anchor=(0.1, 1.1))  # 让图例生效，并设置图例显示位置
    plt.show()


if __name__ == '__main__':
    x, y = get_average_price()
    title = '均价分析图'
    average_price_bar(x, y, title)
