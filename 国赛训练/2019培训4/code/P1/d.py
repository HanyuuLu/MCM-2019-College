# 描述会员分布情况
import sys
import os
from math import pi
from json import dump
sys.path.append('.\\')
from core.const import OUTPUT_PATH
from core.longitudeAndLatitudeConverter import lalConverter
from core.configIO import fetchConfigList
from core.classifier import Classifier
from core.dataReader import dataReader2, dataReader

if __name__ == '__main__':
    configList = fetchConfigList()
    rawData = dataReader2()
    pointRawData = dataReader()[0]
    for key, item in enumerate(rawData):
        rawData[key][1] = lalConverter(rawData[key][1])
    for config in configList:
        centerList = [lalConverter((
            pointRawData[i][1],
            pointRawData[i][2]
        )
        ) for i in config[1]]
        # print(configList)
        # print(rawData)
        # print(centerList)
        collect = list()
        for _ in range(len(centerList)):
            collect.append(list())
        for key, config in enumerate(centerList):
            for i in rawData:
                if (lambda i, config: ((i[1][0] - config[0]) ** 2 + (i[1][1] - config[1]) ** 2) ** 0.5)(i, config) < 5:
                    collect[key].append(i)
        res = list()
        for group in collect:
            res.append(dict())
            res[-1]['num[pcs/km^2]'] = len(group) / (pi * 5 ** 2)
            res[-1]['quota[pcs/km^2]'] = sum([x[2]
                                              for x in group]) / (pi * 5 ** 2)
        fileName = os.path.join(OUTPUT_PATH, 'P01VIP%d.json' % len(collect))
        with open(fileName, 'w') as w:
            dump(res, w)
        print(fileName)
