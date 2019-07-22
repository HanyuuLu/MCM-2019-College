# countour.py
# 等高线绘制
import os
import re
import sys
from json import loads

import matplotlib.pyplot as plt
import numpy as np

sys.path.append('.\\')
from core import const

def pri(x,y, points: dict):
    minList = list()
    for i in points:
        if i is not None:
            dis = (i['E'] - x) ** 2 + (i['N'] - y) ** 2
            if len(minList) < 3:
                minList.append([dis,i])
                continue
            if dis < max([x[0] for x in minList]):
                minList.sort(key=lambda x: x[0])
                del (minList[-1])
                minList.append([dis, i])
    pri = 0
    for i in minList:
        pri += i[1]['price'] * i[0] / sum([x[0] for x in minList])
    return pri



def draw(points: dict):
    delta = 0.02
    x = np.arange(
        const.LONGITUDE_LOWER,
        const.LONGITUDE_UPPER,
        delta
    )
    y = np.arange(
        const.LATITUDE_LOWER,
        const.LATITUDE_UPPER,
        delta
    )
    X, Y = np.meshgrid(x, y)
    row  = list()
    for j in y:
        line = list()
        for i in x:
            line.append(pri(i, j, points))
        row.append(line)
    Z = np.array(row)
    fig, ax = plt.subplots()
    CS = ax.contour(X, Y, Z ,20)
    ax.clabel(CS, inline=True)
    ax.contourf(X, Y, Z, 100, cmap=plt.cm.jet)
    ax.set_title('contour for %d centers'%len(points))

    # plt.show()
    # plt.show()
    fileName = os.path.join(
        const.OUTPUT_PATH, 'P01contour%d.jpg' % len(points))
    plt.savefig(fileName)


if __name__ == '__main__':
    for folder, subFolder, fileNameList in os.walk(const.OUTPUT_PATH):
        # 暂时只需要根目录下的文件
        if folder == const.OUTPUT_PATH:
            for fileName in fileNameList:
                # 匹配坐标文件
                if re.match('^P01point\d+\.json$', fileName):
                    f = os.path.join(folder, fileName)
                    print(f)
                    with open(f, 'r') as w:
                        f = w.read()
                    rawData = loads(f)
                    for key, item in enumerate(rawData):
                        if item is not None:
                            rawData[key] = {
                                'price': sum([x['no'] for x in item])/len([x['no']for x in item]),
                                'E': item[0]['E'],
                                'N': item[0]['N']
                            }
                    draw(rawData)
