import os
from datetime import datetime


def drawGraphs():
    pass


def getData(res: dict) -> list:
    resList = dict()
    resListMobile = dict()
    for value in res:
        for i in res[value].record:
            try:
                key = i[0].strftime("%y%m%d")
                if key in resList:
                    resList[key] += 1
                    if i[1] == 0:
                        resListMobile[key] += 1
                else:
                    resList[key] = 1
                    if i[1] == 0:
                        resListMobile[key] = 1
                    else:
                        resListMobile[key] = 0
            except Exception as e:
                continue
    return (resList, resListMobile)

if __name__ == '__main__':
        # getDataSheet()
    import dataReader
    data = dataReader.getDataSheet()
    res = getData(data)
    print(res)