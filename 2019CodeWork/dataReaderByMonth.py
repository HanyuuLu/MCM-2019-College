import os
import sys
import csv
import dateConvert
import dataType
DataRoot = './data/csv'
# DataRoot = './expdata/'


def getDataSheet():
    global DataRoot
    fileList = []
    for currentDict, subDict, fileName in os.walk(DataRoot):
        for i in fileName:
            fileList.append(os.path.join(currentDict, i))
    print(fileList)
    res = {}
    for i in fileList:
        res[i] = {}
        res[i]["sum"] = 0
        res[i]["mobilePay"] = 0
        print('[info] start to process %s' % i)
        with open(i, 'r') as rawInput:
            input = csv.reader(rawInput)
            for raw in input:
                res[i]["sum"] += 1
                try:
                    if int(float(raw[3])) == 0:
                        res[i]["mobilePay"] += 1
                except Exception as e:
                    continue
    print("[info] data load finished!")
    return res


def str2int(num: str) -> int:
    try:
        return int(float(num))
    except Exception as e:
        return None


if __name__ == '__main__':
    print(getDataSheet())
