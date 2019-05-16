import os
def drawGraphs():
    pass
def numberOfHoursDistributionMap(res: dict) -> list:
    res = list()
    for i in range(25):
        res.append(0)
    for key, value in os.environ.items(res):
        for i in value.record:
            try:
                res[i[0].hour] += 1
            except Exception as e:
                res[24] += 1
    print(res)

