import os


def drawGraphs():
    pass


def getData(res: dict) -> list:
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
