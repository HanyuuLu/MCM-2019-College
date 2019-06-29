import os
import sys
import csv
import dateConvert
import dataType
import time
import copy
DataRoot = './data/csv'
# DataRoot = './expdata/'


def writeToFile(src):
    with open('./data/dataByID.csv', 'w', newline='') as out:
        output =csv.writer(out)
        output.writerows(tuple(src.values()))
    # with open('./data/dataByID.csv', 'a', newline='') as out:
    #     output = csv.writer(out)]
    #     for i in
    #     output.writerows([])

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
    emptyList = []
    for i in range(24):
        emptyList.append(0)
    for i in fileList:
        print('\r[info %2d/%2d, %3.2f%%, %4.2f sec] processing %s'.ljust(60) %
              (count, sum, count/sum*100, time.time()-timeFlag, i),end='')
        with open(os.path.join(currentDict, i), 'r') as rawInput:
            input = csv.reader(rawInput)
            for raw in input:
                try:
                    hour = dateConvert.getDateTime(raw[2]).hour
                except Exception:
                    continue
                id = int(float(raw[0]))
                if id not in res:
                    res[id] = copy.deepcopy(emptyList)
                res[id][hour] += 1
        count += 1
    print('\r                                 ', end='')
    print('\r[info %2d/%2d, %3.2f%%, %4.2f sec] task finished'.ljust(80) %
          (count, sum, count/sum*100, time.time()-timeFlag),end = '')
    return res


def str2int(num: str) -> int:
    try:
       return int(float(num))
    except Exception as e:
        return None


if __name__ == '__main__':
    res = getDataSheet()
    print(len(res))
    writeToFile(res)
