# import os
# import sys
import csv
import random

dataRoot = './data/dataByID.csv'


def distance(item0, item1):
    res = 0
    for i in range(len(item0)):
        res += abs(item0[i] - item1[i])
    return res


def generateKernel(data, kernelNumber):
    kernelList = []
    for _ in range(kernelNumber):
        kernelList.append(data[random.randint(0, len(data))])
    return kernelList


def choose(data, kernelList):
    res = 100000000000000000000000
    for i in kernelList:
        temp = distance(data, i)
        if temp < res:
            key = i
            res = temp
    return kernelList.index(key)


def processData():
    kernelNumber = 6
    print('[info] processing data')
    dataList = []
    originList = []
    for i in range(kernelNumber):
        dataList.append(list())
    # jump = 0
    with open(dataRoot, 'r') as raw:
        input = csv.reader(raw)
        # count = 0
        for i in input:
            originList.append(i)
            # if jump == 100000:
            #     break
            # jump += 1
    for i in range(len(originList)):
        for j in range(len(originList[i])):
            originList[i][j] = int(originList[i][j])
    kernelList = generateKernel(originList, kernelNumber)
    for i in originList:
        dataList[choose(i, kernelList)].append(i)
    return dataList


def average(src):
    print('[info]calculating average')
    res = []
    for i in src:
        temp = []
        for _ in range(24):
            temp.append(0)
        for j in i:
            for key in range(24):
                temp[key] += j[key]
        for k in range(24):
            temp[k] /= len(i)
        res.append(temp)
    return res


def draw(src):
    print('[info] drawing')
    from matplotlib import pyplot as plt
    import math
    for i in range(len(src)):
        plt.subplot(2, math.ceil(len(src) / 2), i+1)
        plt.plot([x for x in range(24)], src[i], 'b-')
    plt.show()


if __name__ == '__main__':
    raw = processData()
    pro = average(raw)
    draw(pro)
