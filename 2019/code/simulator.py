import datetime
import time

# import math
import numpy as np

import conf
import dataloader
import role
import json

# import matplotlib.pyplot as plt
arriveData = dataloader.arriveData()
departData = dataloader.departData()


def genInputTaxiSequence() -> list:
    pass


def genDepartList(count: int, timeOffset: int):
    con = conf.Conf()
    np.random.seed(0)
    res = list()
    while len(res) < count:
        t = int(np.random.normal(con.departMiu, con.departSigma, 1)[0])
        if t > con.departLeft and t < con.departRight:
            res.append(int(t + timeOffset))
    return res


def genArriveList(count: int, timeOffset: int):
    con = conf.Conf()
    np.random.seed(0)
    res = list()
    while len(res) < count*con.arriveLRate:
        t = int(np.random.normal(con.arriveLMiu, con.arriveLSigma, 1)[0])
        if t > con.arriveLLeft and t < con.arriveLRight:
            res.append(int(t + timeOffset))
    while len(res) < count:
        t = int(np.random.normal(con.arriveHMiu, con.arriveHSigma, 1)[0])
        if t > con.arriveHLeft and t < con.arriveHRight:
            res.append(int(t+timeOffset))
    return res


def mode2people(src: str):
    return 200


def genDepartTimeLine():
    con = conf.Conf()
    timeLine = list()
    for i in departData:
        timeLine.extend(
            genDepartList(
                int(mode2people(i['机型'])*con.departRate/con.taxiAvgPeople),
                int(time.mktime(i['计划出发时间'].timetuple()))/60
            )
        )
    timeLine.sort()
    return timeLine


def genArriveTimeLine():
    con = conf.Conf()
    timeLine = list()
    for i in arriveData:
        timeLine.extend(
            genArriveList(
                int(mode2people(i['机型'])*con.departRate/con.taxiAvgPeople),
                int(time.mktime(i['计划到达时间'].timetuple()))/60
            )
        )
    timeLine.sort()
    return timeLine


def minuteStamp(src: datetime.datetime)->int:
    return int(time.mktime(src.timetuple())/60)


class Simulator:
    def __init__(self):
        # 航班信息
        self.arriveData = arriveData
        self.departData = departData
        # 时间线
        self.departTimeLine = genDepartTimeLine()
        self.arriveTimeLine = genArriveTimeLine()
        self.conf = conf.Conf()
        self.keyTime = None

    def train(self):
        log = dict()
        logList = list()
        log['total passenger'] = len(self.arriveTimeLine)
        log['total taxi'] = len(self.departTimeLine)
        self.keyArriveTimeLine = 0
        self.keyDepartIimeLine = 0
        self.passengerQuery = list()
        self.carQuery = list()
        self.tempCarQuery = list()
        for self.keyTime in range(
                minuteStamp(self.conf.startDate),
                minuteStamp(self.conf.endDate),
                1):
            if self.keyTime % 60 == 0:
                print(self.keyTime)
            self.update(self.driverDetermineKnown)
            res = dict()
            res['time'] = time.strftime(
                "%Y-%m-%d %H:%M:%S", time.localtime(self.keyTime*60))
            res['passenger'] = len(self.passengerQuery)
            res['taxi in ready'] = len(self.tempCarQuery)
            res['taxi at depart'] = len(self.carQuery)
            logList.append(res)
            log['his'] = logList
        with open('log.json', 'w') as w:
            json.dump(log, w)

    def update(self, choiceFunction):
        # 更新到达乘客信息
        while self.keyArriveTimeLine < len(self.arriveTimeLine) and \
                self.arriveTimeLine[self.keyArriveTimeLine] <= self.keyTime:
            self.passengerQuery.append(role.Passenger(
                self.arriveTimeLine[self.keyArriveTimeLine]
            ))
            self.keyArriveTimeLine += 1
        # 更新到达出租车信息
        while self.keyDepartIimeLine < len(self.departTimeLine) and \
                self.departTimeLine[self.keyDepartIimeLine] <= self.keyTime:
            self.tempCarQuery.append(role.Taxi(
                self.departTimeLine[self.keyDepartIimeLine]))
            self.keyDepartIimeLine += 1
        # 推进蓄车池队列
        for p, i in enumerate(self.tempCarQuery[:]):
            if i.loadTime + \
                self.conf.processTime['depart2choice'] \
                    <= self.keyTime:
                if choiceFunction():
                    self.carQuery.append(i)
                self.tempCarQuery.remove(i)

        # 载客
        if self.keyTime % self.conf.processTime['waitPassenger']:
            maxCon = min(len(self.carQuery), len(
                self.passengerQuery), self.conf.patch)
            # 有载客行为
            if maxCon > 0:
                for i in range(maxCon):
                    del self.carQuery[0]
                    del self.passengerQuery[0]
            else:
                # 无出租车
                if len(self.carQuery) == 0:
                    for p, i in enumerate(self.passengerQuery[:]):
                        if i.waitTime is None:
                            i.waitTime = self.keyTime
                        else:
                            if self.keyTime - i.waitTime > \
                                    self.conf.maxWaitTime:
                                del self.passengerQuery[p]
                # 无乘客
                else:
                    # maxT = max(self.conf)
                    for i in self.carQuery[:]:
                        if i.waitTime is None:
                            i.waitTime = self.keyTime
                        else:
                            if i.waitTime + \
                                    self.conf.maxWaitTime < self.keyTime:
                                for _ in range(self.conf.patch):
                                    del self.carQuery[0]
                                break

    def driverDetermine(self) -> bool:
        return True

    def driverDetermineKnown(self) -> bool:
        # 乘客已在队列中
        if len(self.passengerQuery) > len(self.carQuery):
            waitTime = self.keyTime % self.conf.processTime['waitPassenger'] +\
                (len(self.carQuery)+1)//self.conf.patch * \
                self.conf.processTime['waitPassenger']
        else:
            waitTime = max(
                self.keyTime % self.conf.processTime['waitPassenger'] +
                (len(self.carQuery)+1)//self.conf.patch *
                self.conf.processTime['waitPassenger'],
                self.arriveTimeLine
                [
                    self.keyArriveTimeLine +
                    len(self.carQuery) + 1 -
                    len(self.passengerQuery)
                ]
            )
        if waitTime > self.conf.defaultWaitTime:
            return False
        else:
            return True


if __name__ == '__main__':
    exp = Simulator()
    exp.train()
