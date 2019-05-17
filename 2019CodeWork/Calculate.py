import os
from datetime import datetime

def getDays(res: dict) -> list:
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

def getHours(res: dict) -> list:
    resList = list()
    for i in range(25):
        resList.append(0)
    for value in res:
        for i in res[value].record:
            try:
                resList[i[0].hour] += 1
            except Exception as e:
                resList[24] += 1
    return resList

def getWeeks(res: dict) -> list:
    resList = dict()
    resListMobile = dict()
    for value in res:
        for i in res[value].record:
            try:
                key = i[0].weekday()
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
    res = getHours(data)
    res = getWeeks(data)
    res = getDays(data)
    print(res)