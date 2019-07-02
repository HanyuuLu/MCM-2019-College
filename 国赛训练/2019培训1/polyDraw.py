import numpy as np
import matplotlib.pyplot as plt
def draw(x,y,yvals):
    #绘图
    plot1 = plt.plot(x, y, 's',label='original values')
    plot2 = plt.plot(x, yvals, 'r',label='polyfit values')
    plt.xlabel('x')
    plt.ylabel('y')
    plt.legend(loc=4) #指定legend的位置右下角
    plt.title('polyfitting')
    plt.show()