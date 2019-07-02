import numpy as np
import matplotlib.pyplot as plt
def draw(data):
    #绘图

    plot = list()
    plt.rcParams['font.sans-serif'] = ['SimHei']  # 用来正常显示中文标签
    plt.rcParams['axes.unicode_minus'] = False  # 用来正常显示负号
    plot.append(plt.plot(data[0][0],data[0][1], '-',label='-8°/s'))
    plot.append(plt.plot(data[1][0],data[1][1], '-',label='-4°/s'))
    plot.append(plt.plot(data[2][0],data[2][1], '-',label='0°/s'))
    plot.append(plt.plot(data[3][0],data[3][1], '-',label='+2°/s'))
    plot.append(plt.plot(data[4][0],data[4][1], '-',label='+4°/s'))
    plt.xlabel('y')
    plt.ylabel('z')
    plt.legend(loc=4) #指定legend的位置右下角
    plt.title('[初始角速度]对运动的影响')
    plt.show()
