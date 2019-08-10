import math
import os
from json import dump, load

from CONST import OUTPUT
from dataReader import fetchData


def fetchSXLtoJSON():
    '''
    将市销率数值提取到rawData[12].json中
    '''
    rawData1 = fetchData(0)
    rawData2 = fetchData(1)

    data1 = dict()
    for key in rawData1:
        data1[key] = list()
        for i in rawData1[key]:
            data1[key].append(i[3])
    data2 = dict()
    for key in rawData2:
        data2[key] = list()
        for i in rawData2[key]:
            data2[key].append(i[2])
    with open(os.path.join(OUTPUT, 'rawData1.json'), 'w') as w:
        dump(data1, w)
    with open(os.path.join(OUTPUT, 'rawData2.json'), 'w') as w:
        dump(data2, w)


def avgCalc():
    '''
    计算算术平均和移动平均
    '''
    data1 = None
    data2 = None
    fileName = os.path.join(OUTPUT, 'rawData1.json')
    with open(fileName, 'r') as r:
        data1 = load(r)
    fileName = os.path.join(OUTPUT, 'rawData2.json')
    with open(fileName, 'r') as r:
        data2 = load(r)
    pass
    data = (data1, data2)

    for key, data in enumerate(data):
        # 结果字典
        res = dict()
        # 平均值字典
        avg = dict()
        #  指数平均列表
        ewma = list()

        res['note'] = "各年份市销率除零平均值,avg:平均；ewma：夹权指数平均"
        for year in data:
            dataSum = 0
            count = 0
            for i in data[year]:
                if i > 0:
                    dataSum += math.log(i)
                    count += 1
            avg[year] = math.e**(dataSum / count)
        eAvg = 0
        eRate = 0.9
        tmp = list(avg.values())
        tmp.reverse()
        for i in tmp:
            eAvg = eRate * i + (1 - eRate) * eAvg
            ewma.append(eAvg)
        res['avgList'] = avg
        res['ewmaList'] = ewma
        res['avg'] = sum([avg[i] for i in avg]) / len(avg)
        res['ewma'] = eAvg
        res['溢价'] = ewma[-1]/avg['2018']
        fileName = os.path.join(OUTPUT, 'avg%d.json' % key)
        with open(fileName, 'w') as w:
            dump(res, w)


if __name__ == '__main__':
    avgCalc()
