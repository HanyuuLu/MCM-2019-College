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
        print('[info] start to process %s' % i)
        with open(i, 'r') as rawInput:
            input = csv.reader(rawInput)
            for raw in input:
                try:
                    id = int(float(raw[0]))
                except Exception as e:
                    continue
                if int(id) in res:
                    temp = [dateConvert.getDateTime(raw[2]),    # 乘车日期
                            str2int(raw[3])  # 支付类型
                            ]
                    # print(temp)
                    res[id].record.append(temp)
                else:
                    res[id] = dataType.UserRecord()
                    res[id].uuid = id
                    temp = [dateConvert.getDateTime(raw[2]),    # 乘车日期
                            str2int(raw[3])  # 支付类型
                            ]
                    # print(temp)
                    res[id].record.append(temp)
    print("[info] data load finished!")
    return res


def str2int(num: str) -> int:
    try:
        return int(float(num))
    except Exception as e:
        return None


if __name__ == '__main__':
    pass