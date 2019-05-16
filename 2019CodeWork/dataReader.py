import os
import sys
import csv
import dateConvert
DataRoot = './data/csv'

def getDataSheet():
    global DataRoot
    fileList = []
    for currentDict, subDict, fileName in os.walk(DataRoot):
        for i in fileName:
            fileList.append(os.path.join(currentDict, i))
    print(fileList)
    res = {}
    for i in fileList:
        print('[info] start to process %s' % i)
        with open(i, 'r') as rawInput:
            input = csv.reader(rawInput)
            for raw in input:
                try:
                    id = int(float(raw[0]))
                except Exception as e:
                    print(e)
                    continue
                if int(id) in res:
                    res[id].append
                    ([
                        dateConvert.getdate(raw[2]),    # 乘车日期
                        int(raw[3])                     # 支付类型
                    ])


if __name__ == '__main__':
    getDataSheet()
