import matplotlib
import pylab
import os
import sys
import csv
import dateConvert
import dataType
import time
import math
import datetime
DataRoot = './data/csv'
# DataRoot = './expdata/'

def getWeekdaysByFilename(filename: str) -> int:
    # print(datetime.datetime(int(filename[0:4]), int(
        # filename[4:6]), int(filename[6:8])).weekday())
    return datetime.datetime(int(filename[0:4]), int(filename[4:6]), int(filename[6:8])).weekday()

def getDataSheet():
    timeFlag = time.time()
    global DataRoot
    fileList = []

    for currentDict, subDict, fileName in os.walk(DataRoot):
        for i in fileName:
            fileList.append(i)
    count = 0
    sum = len(fileList)
    resSum = {}
    resMobile = {}
    resNull = {}
    resNotMobile = {}
    for i in fileList:
        print('\r[info %2d/%2d, %3.2f%%, %4.2f sec] processing %s' %
              (count, sum, count/sum*100, time.time()-timeFlag, i), end='')
        with open(os.path.join(currentDict, i), 'r') as rawInput:
            input = csv.reader(rawInput)
            filter = {'0.0': resMobile, 'Null': resNull}
            for raw in input:
                try:
                    # print(i[4:6])
                    # key = dateConvert.getDateTime(raw[2]).month
                    key = getWeekdaysByFilename(i)
                    # print(key)
                    if key not in resSum:
                        resSum[key] = 0
                        resMobile[key] = 0
                        resNull[key] = 0
                        resNotMobile[key] = 0
                    resSum[key] += 1
                    filter[raw[3]][key] += 1
                except Exception:
                    continue
        count += 1
    print('[info %d/%d, %.2f%%, %.2f sec] task finished' %
          (count, sum, count / sum * 100, time.time() - timeFlag))
    print('resSum', resSum)
    print('resMobile', resMobile)
    print('resNull', resNull)
    for i in resSum:
        resMobile[i] += resNull[i]
        resNotMobile[i] = resSum[i] - resMobile[i]
    resMobile = list(resMobile.values())
    resNotMobile = list(resNotMobile.values())

    return resMobile, resNotMobile


def str2int(num: str) -> int:
    try:
       return int(float(num))
    except Exception as e:
        return None


def draw(res):
    from matplotlib import pyplot as plt
    # %matplotlib inline
    plt.rcParams['font.sans-serif'] = ['SimHei']  # 用来正常显示中文标签
    plt.rcParams['axes.unicode_minus'] = False  # 用来正常显示负号

    # Pie chart, where the slices will be ordered and plotted counter-clockwise:
    labels = '移动支付', '非移动支付'
    explode = (0, 0.1)
    fig = []
    countNumber = len(res[0])
    for i in range(countNumber):
        fig.append(plt.subplot(3, math.ceil(countNumber/3), i+1))
        plt.pie(
            [res[0][i], res[1][i]],
            labels=labels,
            explode=explode,
            autopct='%1.2f%%',
            shadow=True,
            startangle=90,
            textprops={'size': 'large'}
        )
        fig[-1].set_title(i)
    plt.show()


if __name__ == '__main__':
    res = getDataSheet()
    draw(res)
