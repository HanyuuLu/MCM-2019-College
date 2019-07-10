import math
import matplotlib.pyplot as plt
import numpy

def draw(data):
    plt.rcParams['font.sans-serif'] = ['SimHei']
    plt.rcParams['axes.unicode_minus'] = False
    x = list(range(100))
    y0 = data[0]
    y1 = data[1]
    plt.plot(x, y0, label='住院人数')
    plt.plot(x, y1, label='出院人数')
    plt.ylabel("人数")
    plt.xlabel("距离7月1日天数")
    plt.legend(loc='lower right')
    plt.title("住院出院人数随天数分布图")
    plt.show()
