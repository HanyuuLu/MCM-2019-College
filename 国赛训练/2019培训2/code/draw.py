import math
import matplotlib.pyplot as plt
import numpy


def functionA(x):
    if x <= 6.30 and x >= 0:
        return 0
    elif x >= 6.3 and x <= 14.1:
        return 3.57*math.cosh(0.28*x-1.76)-3.57
    else:
        return 0


def functionB(x):
    if x >= 0 and x <= 16.9:
        return 14.68*math.cosh(0.068*x+0.078)-14.68


if __name__ == '__main__':
    plt.rcParams['font.sans-serif'] = ['SimHei']
    plt.rcParams['axes.unicode_minus'] = False
    x0 = list()
    y0 = list()
    x1 = list()
    y1 = list()
    for x in numpy.arange(0, 14.1, 1e-3):
        x0.append(x)
        y0.append(functionA(x))
    for x in numpy.arange(0, 16.9, 1E-3):
        x1.append(x)
        y1.append(functionB(x))
    plt.plot(x0, y0, label='风速：12m/s')
    plt.plot(x1, y1, label='风速：24m/s')
    plt.ylabel("y")
    plt.xlabel("x")
    plt.legend(loc='lower right')
    plt.title("锚链形状示意图")
    plt.show()
