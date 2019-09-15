import datetime
import time

from copy import deepcopy
# import math
import numpy as np
from scipy.stats import norm

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


with open('./plane.json', 'r') as r:
    planeModule = json.load(r)


def mode2people(src: str):
    return planeModule[src]


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
                int(mode2people(i['机型'])*con.arriveRate/con.taxiAvgPeople),
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
        self.log = dict()
        self.driverLog = list()
        self.logList = list()
        self.logListPassenger = list()
        self.log['报告产生时间'] = time.strftime(
            "%Y-%m-%d %H:%M:%S", time.localtime(time.time()))
        self.log['total passenger'] = len(self.arriveTimeLine)
        self.log['total taxi'] = len(self.departTimeLine)
        # 统计需求2
        self.driverALLProfits = 0
        self.driverALLTimes = 0

        self.keyClipWindowDepartLeft = 0
        self.keyClipWindowDepartRight = 0
        self.keyClipWindowArriveLeft = 0
        self.keyClipWindowArriveRight = 0
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
                proc = ((self.keyTime+1 - minuteStamp(self.conf.startDate)) /
                        (minuteStamp(self.conf.endDate) -
                         minuteStamp(self.conf.startDate)))*100
                print("%s\n[%.2f%%]" % (self.keyTime, proc), end="\r")
            # self.update(self.driverDetermineKnown)
            self.update(self.driverDetermine)
            res = dict()
            res['time'] = time.strftime(
                "%Y-%m-%d %H:%M:%S", time.localtime(self.keyTime*60))
            res['passenger'] = len(self.passengerQuery)
            res['taxi in ready'] = len(self.tempCarQuery)
            res['taxi at depart'] = len(self.carQuery)
            self.logList.append(res)
        self.log['各列表历史记录'] = self.logList
        self.log['接单司机单位时间收入'] = self.driverLog
        self.log['司机盈利状况'] = self.driverALLProfits / \
            self.driverALLTimes * 60
        self.log['带客司机平均等待时间'] = sum(
            [i['costTime'] for i in self.driverLog]) / len(self.driverLog)
        self.log['上车乘客等待时间'] = self.logListPassenger
        self.log['上车乘客平均等待时间'] = \
            sum([i['costTime'] for i in self.logListPassenger]) / \
            len(self.logListPassenger)
        with open('log.json', 'w') as w:
            json.dump(self.log, w)

    def update(self, choiceFunction):
        # 更新航班信息提示指针
        while self.keyClipWindowArriveLeft < len(self.arriveData) and \
            minuteStamp(
            self.arriveData[self.keyClipWindowArriveLeft]
                ['计划到达时间']) < self.keyTime +\
                self.conf.clipWindowArriveLeft:
            self.keyClipWindowArriveLeft += 1
        while self.keyClipWindowArriveRight < len(self.arriveData) and \
                minuteStamp(
                    self.arriveData[self.keyClipWindowArriveRight]
                    ['计划到达时间']) < self.keyTime + \
                self.conf.clipWindowArriveRight:
            self.keyClipWindowArriveRight += 1
        while self.keyClipWindowDepartLeft < len(self.departData) and \
                minuteStamp(
                    self.departData[self.keyClipWindowDepartLeft]
                    ['计划出发时间']) < self.keyTime + \
                self.conf.clipWindowDepartLeft:
            self.keyClipWindowDepartLeft += 1
        while self.keyClipWindowDepartRight < len(self.departData) and \
                minuteStamp(
                    self.departData[self.keyClipWindowDepartRight]
                    ['计划出发时间']) < self.keyTime + \
                self.conf.clipWindowDepartRight:
            self.keyClipWindowDepartRight += 1

        # 更新到达乘客信息
        while self.keyArriveTimeLine < len(self.arriveTimeLine) and \
                self.arriveTimeLine[self.keyArriveTimeLine] <= self.keyTime:
            if len(self.passengerQuery) < self.conf.maxWaitingQueue:
                self.passengerQuery.append(role.Passenger(
                    self.arriveTimeLine[self.keyArriveTimeLine]))
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
                    self.carQuery.append(deepcopy(i))
                self.tempCarQuery.remove(i)
        # 载客
        if self.keyTime % self.conf.processTime['waitPassenger'] == 0:
            maxCon = min(len(self.carQuery), len(
                self.passengerQuery), self.conf.patch)
            # 有载客行为
            if maxCon > 0:
                for i in range(maxCon):
                    lastCar = self.carQuery[0]
                    lastPassenger = self.passengerQuery[0]

                    # 统计需求
                    self.driverLog.append(
                        {
                            "time": lastCar.loadTime,
                            "costTime": self.keyTime - lastCar.loadTime,
                            "profitsPerHour":
                            110/(45+(self.keyTime - lastCar.loadTime))*60
                        }
                    )
                    self.logListPassenger.append(
                        {
                            "time": lastPassenger.loadTime,
                            "costTime": self.keyTime-lastPassenger.loadTime
                        }
                    )

                    costTime = self.keyTime - lastCar.loadTime+self.conf.toCity
                    self.driverALLProfits += self.conf.averageCash - \
                        self.conf.averageProfits * \
                        (costTime) / 60
                    self.driverALLTimes += costTime

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
                                self.passengerQuery.remove(i)
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

                                    # 统计需求
                                    lastCar = self.carQuery[0]
                                    costTime = self.keyTime - lastCar.loadTime+self.conf.toCity
                                    self.driverALLProfits -= \
                                        self.conf.averageProfits * \
                                        (costTime) / 60
                                    self.driverALLTimes += costTime

                                    del self.carQuery[0]
                                break

    def driverDetermine(self) -> bool:
        arriveData, departData = self.clipData()
        inCounter = 0
        for i in arriveData:
            inCounter +=\
                mode2people(i['机型']) * self.conf.arriveRate / \
                self.conf.taxiAvgPeople * norm.cdf(
                    (self.keyTime-minuteStamp(i['计划到达时间']) -
                     self.conf.arriveLMiu)/self.conf.arriveLSigma
                )
        outCounter = 0
        for i in departData:
            outCounter +=\
                mode2people(i['机型']) * self.conf.departRate / \
                self.conf.taxiAvgPeople
        maxOutCounter = \
            (
                self.conf.clipWindowDepartRight - self.conf.clipWindowDepartLeft
            ) / \
            self.conf.processTime['waitPassenger'] * self.conf.patch
        outCounter = max(outCounter, maxOutCounter)
        if (inCounter - outCounter > len(self.carQuery)):
            return True
        else:
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
                    len(self.carQuery) -
                    len(self.passengerQuery)
                ]
            )
        if waitTime > self.conf.defaultWaitTime:
            return False
        else:
            return True

    def clipData(self):
        arriveData = self.arriveData[
            self.keyClipWindowArriveLeft:
            self.keyClipWindowArriveRight
        ]
        departData = self.departData[
            self.keyClipWindowDepartLeft:
            self.keyClipWindowDepartRight
        ]
        return arriveData, departData


if __name__ == '__main__':
    exp = Simulator()
    exp.train()
