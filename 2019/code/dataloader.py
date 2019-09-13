import json
import time
import datetime
import conf
conf = conf.Conf()


def arriveData() -> dict:
    dayOffset = 0
    last = 0
    with open('./到达.json') as r:
        rawData = json.load(r)
    for i in rawData:
        h = int((i['计划到达时间'])[:2])
        m = int((i['计划到达时间'])[-2:])
        if h < last:
            dayOffset += 1
            last = 0
        else:
            last = h
        timeOffset = datetime.timedelta(days=dayOffset, hours=h, minutes=m)
        i['计划到达时间'] = conf.initDate + timeOffset
    return rawData


def departData() -> dict:
    dayOffset = 0
    last = 0
    with open('./出发.json') as r:
        rawData = json.load(r)
    for i in rawData:
        h = int((i['计划出发时间'])[:2])
        m = int((i['计划出发时间'])[-2:])
        if h < last:
            dayOffset += 1
            last = 0
        else:
            last = h
        timeOffset = datetime.timedelta(days=dayOffset, hours=h, minutes=m)
        i['计划出发时间'] = conf.initDate + timeOffset
    return rawData


if __name__ == '__main__':
    data = arriveData()
    dataD = departData()
    print(dataD[33])
