import os
import sys
import csv
import dateConvert
import dataType
import time
DataRoot = './data/csv'
# DataRoot = './expdata/'


def getDataSheet():
    timeFlag = time.time()
    global DataRoot
    fileList = []

    for currentDict, subDict, fileName in os.walk(DataRoot):
        for i in fileName:
            fileList.append(i)
    count = 0
    sum = len(fileList)
    res = {}
    for i in fileList:
        print('[info %2d/%2d, %3.2f%%, %4.2f sec] processing %s' % (count, sum, count/sum*100, time.time()-timeFlag, i ))
        with open(os.path.join(currentDict, i), 'r') as rawInput:
            key = i[:8]
            input = csv.reader(rawInput)
            res[key] = {'mobile': 0, 'card': 0, 'other': 0, 'null': 0}
            filter = {'0.0':'mobile','1.0':'card', 'Null': 'null'}
            for raw in input:
                if raw[3] in filter:
                    res[key][filter[raw[3]]] += 1
                else:
                    if raw[0] == 'ID':
                        continue
                    res[key]['other'] += 1
        count += 1
    print('[info %d/%d, %.2f%%, %.2f sec] task finished' %
              (count, sum, count/sum*100, time.time()-timeFlag))
    return res


def str2int(num: str) -> int:
    try:
       return int(float(num))
    except Exception as e:
        return None


if __name__ == '__main__':
    print(getDataSheet())
