# # 画坐标图
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.font_manager import FontProperties
import pylab
import math


def One():
    """指用numpy库里的linspace函数来间隔采样，从0到10之间取出500个数"""
    x = np.linspace(0, 10, 500)
    """
    指曲线上的点分为无数个“第一段+第二段”的组合，
    第一段是先显示10 个点再隐藏5个点,
    第二段是先显示100个点再隐藏5个点 ，
    依次循环“第一段+第二段”的组合；
    """
    dashes = [100, 50, 1000, 50]
    """
    用子图绘制函数subplots来绘图的步骤，
    函数返回一个figure图像和一个子图ax的array列表。括号里可以填参数，
    分别代表子图的行数和列数，在这里缺省了（在这张图的绘制里形参括号里填(1,1)和缺省的效果是一样的，但填(2,2)就出bug了）
    """
    fig, ax = plt.subplots()
    """
    画曲线1，横轴变量x映射成的y是正弦sin函数，线条样式是’–’，宽度是2，
    第一条线的名称是’Dashes set retroactively’(破折号追溯？迷之翻译。。。)
    """
    line1 = ax.plot(x, np.sin(x), '--', linewidth=2,
                    label='Dashes set retroactively', color='r')

    """
    画曲线2，这里可以看到plot函数的参数设置有所改变，映射的y对象变成负正弦函数，dashes样式也改变了；
    """
    line2 = ax.plot(x, -1 * np.cos(x), dashes=[300, 50, 100, 50],
                    label='Dashes set proactively', color='cyan')

    """
    这行代码用来在图中显示曲线1与曲线2的”label”信息。
    """
    ax.legend(loc='lower right')

    """
    显示图
    """
    return plt.show()


def two():
    # 案例：绘制正弦曲线
    # x = np.linspace(0, 100, 200)  #正弦曲线的x坐标，用List,tuple都行
    x = np.arange(100)
    y = np.sin(x)  # 正弦曲线的y坐标 ， 与X个数一直
    fig = plt.figure()  #
    ax = fig.subplots()  # 等价于 fig, ax = plt.subplots()
    line1 = ax.plot(x, y, '-', linewidth=2, label='line1', color='pink')  # plot画坐标
    ax.legend(loc='lower right')  # label 放在哪里
    plt.show()

    # subplot函数对正余弦函数图像使用子图绘制，并用ylabel ,xlabel 来添加 轴
    x = np.linspace(0, 10, 1000)
    y = np.sin(x)
    z = np.cos(x ** 2)
    plt.figure()
    plt.subplot(3, 1, 1)
    plt.plot(x, y, label='$sin(x)$', color="red", linewidth=2)
    plt.ylabel('y volt')

    plt.subplot(3, 1, 2)
    plt.plot(x, y, label='$sin(x)$', color="red", linewidth=2)
    plt.ylabel('y volt')

    plt.subplot(3, 1, 3)
    plt.plot(x, z, label="$cos(x^2)$", color="blue", linewidth=1)
    plt.ylabel('z volt')
    plt.xlabel("Time(s)")
    return plt.show()


# #中文使用
def three():
    font_set = FontProperties(fname=r"c:\windows\fonts\simsun.ttc", size=16)
    x = np.linspace(0, 10, 100)
    y = np.sin(x)
    fig = plt.figure()
    ax = plt.subplot(1, 1, 1)  #
    line1 = ax.plot(x, y, '-', linewidth=2, label='line1')
    plt.title(u'标题', fontproperties=font_set)
    plt.ylabel(r'y轴', fontproperties=font_set)
    plt.xlabel(r'x轴', fontproperties=font_set)
    ax.legend(loc='lower right')  # label 放在哪里
    return plt.show()


def four():
    # 添加文字注释

    x = np.linspace(0, 10, 100)
    y = np.sin(x)
    z = np.cos(x ** 2)
    fig = plt.figure(figsize=(8, 4))
    ax = fig.add_subplot(211)
    plt.subplot(2, 1, 1)
    plt.plot(x, y, label='$sin(x)$', color="red", linewidth=2)
    plt.ylabel('y volt')
    plt.subplot(2, 1, 2)
    plt.plot(x, z, label="$cos(x^2)$", color="blue", linewidth=1)
    ax.annotate('sin(x)', xy=(2, 1), xytext=(3, 1.5),
                arrowprops=dict(facecolor='black', shrink=0.05))
    ax.set_ylim(-2, 2)  # 限制 211 子图的y坐标范围
    return plt.show()


def five():
    # 画散点图
    x = [5, 6, 7, 8]
    y = [7, 3, 8, 3]
    plt.scatter(x, y)
    return plt.show()


def six():
    # 饼图
    fig = plt.figure()
    x = [1, 3, 5, 6, 7]
    y = [1, 4, 5, 8, 6]
    data = np.random.randint(1, 11, 5)
    # # 设置第二个饼块的偏移量是0.2
    plt.pie(x, explode=[0, 0, 0.2, 0, 0])
    # x可以替换为任意5个数的列表
    plt.title(u"pie")
    fig.set_facecolor('pink')
    return plt.show()


def seven():
    # 用另外一种子图的部署方式方式 （subplot 或add_subpolt()是均匀分割 figure  ）
    # 用  plt.add_axes（坐标） 直接指定区域位置

    fig = plt.figure()
    x = [1, 2, 3, 4, 5, 6, 7]
    y = [1, 3, 4, 2, 5, 8, 6]
    left, bottom, width, height = 0.1, 0.1, 0.8, 0.8
    ax1 = fig.add_axes([left, bottom, width, height])
    ax1.plot(x, y, 'r')
    ax1.set_title('area1')
    left, bottom, width, height = 0.2, 0.6, 0.25, 0.25
    ax2 = fig.add_axes([left, bottom, width, height])
    ax2.plot(x, y, 'b')
    ax2.set_title('area2')
    return plt.show()


def eight():
    # 两种方法混用

    fig = plt.figure()
    x = [1, 2, 3, 4, 5, 6, 7]
    y = [1, 3, 4, 2, 5, 8, 6]
    ax1 = fig.add_axes([0.1, 0.1, 0.8, 0.8])
    ax1.plot(x, y, 'r')
    ax1.set_title('area1')
    ax2 = fig.add_axes([0.2, 0.6, 0.25, 0.25])
    ax2.plot(x, y, 'b')
    ax2.set_title('area2')
    ax3 = fig.add_subplot(2, 2, 4)
    ax3.plot(x, y, 'y')
    ax3.set_title('area3')
    return plt.show()


def nine():
    # 运用pylab 模块绘制正弦函数

    x_values = []
    y_values = []
    num = 0.0
    while num < math.pi * 4:
        y_values.append(math.sin(num))
        x_values.append(num)
        num += 0.1
    # now plot
    pylab.plot(x_values, y_values, 'ro')
    return pylab.show()


def ten():
    ## matplotlib官网
    # Fixing random state for reproducibility
    np.random.seed(19680801)
    N = 100
    r0 = 0.6
    x = 0.9 * np.random.rand(N)
    y = 0.9 * np.random.rand(N)
    area = (20 * np.random.rand(N)) ** 2  # 0 to 10 point radii
    c = np.sqrt(area)
    r = np.sqrt(x ** 2 + y ** 2)
    area1 = np.ma.masked_where(r < r0, area)
    area2 = np.ma.masked_where(r >= r0, area)
    plt.scatter(x, y, s=area1, marker='^', c=c)
    plt.scatter(x, y, s=area2, marker='o', c=c)
    # Show the boundary between the regions:
    theta = np.arange(0, np.pi / 2, 0.01)
    plt.plot(r0 * np.cos(theta), r0 * np.sin(theta))
    return plt.show()


def eleven():
    # 柱状图
    labels = ['G1', 'G2', 'G3', 'G4', 'G5']
    men_means = [20, 35, 30, 35, 27]
    women_means = [25, 32, 34, 20, 25]
    men_std = [2, 3, 4, 1, 2]
    women_std = [3, 5, 2, 3, 3]
    width = 0.35  # the width of the bars: can also be len(x) sequence

    fig, ax = plt.subplots()

    ax.bar(labels, men_means, width, yerr=men_std, label='Men')
    ax.bar(labels, women_means, width, yerr=women_std, bottom=men_means,
           label='Women')

    ax.set_ylabel('Scores')
    ax.set_title('Scores by group and gender')
    ax.legend()

    return plt.show()


def twelve():
    ##3D图
    from matplotlib import cbook
    from matplotlib import cm
    from matplotlib.colors import LightSource
    import matplotlib.pyplot as plt
    import numpy as np

    dem = cbook.get_sample_data('jacksboro_fault_dem.npz', np_load=True)
    z = dem['elevation']
    nrows, ncols = z.shape
    x = np.linspace(dem['xmin'], dem['xmax'], ncols)
    y = np.linspace(dem['ymin'], dem['ymax'], nrows)
    x, y = np.meshgrid(x, y)

    region = np.s_[5:50, 5:50]
    x, y, z = x[region], y[region], z[region]

    fig, ax = plt.subplots(subplot_kw=dict(projection='3d'))

    ls = LightSource(270, 45)
    # To use a custom hillshading mode, override the built-in shading and pass
    # in the rgb colors of the shaded surface calculated from "shade".
    rgb = ls.shade(z, cmap=cm.gist_earth, vert_exag=0.1, blend_mode='soft')
    surf = ax.plot_surface(x, y, z, rstride=1, cstride=1, facecolors=rgb,
                           linewidth=0, antialiased=False, shade=False)
    ax.set_xticks([])
    ax.set_yticks([])
    ax.set_zticks([])
    return plt.show()


One()
two()
three()
four()
five()
six()
seven()
eight()
nine()
ten()
eleven()
twelve()
