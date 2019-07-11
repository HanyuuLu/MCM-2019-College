from datetime import datetime, timedelta
from copy import deepcopy
from math import e as E
from random import randint
from statistics import Const

from dataReader import dataReader


class InpatientSystem(Const):
    def __init__(self):
        super().__init__()
        # 数据表中数据
        self.rawData = dataReader()[0]
        # 数据表中总人数
        self.SUM_PATIENT = len(self.rawData)
        # 开始日期基准点
        self.INITIAL_DATE = datetime(2008, 6, 30)
        # 更换策略日期，病房统计率开始点
        self.DIVIDED_DATE = datetime(2008, 8, 8)
        # 病房统计率结束点
        self.FINSIH_RATE_DATE = datetime(2008, 9, 11)
        # 结束时间
        self.FINISH_DATE = datetime(2008, 10, 10)
        # 老化门槛
        self.AGING_JUDGING = 10
        # 床位数
        self.BED_COUNT = 79
        # 今日日期
        self.now = self.INITIAL_DATE
        # 每日换人病床统计数
        self.changeCountLog = list()
        # 当前病床病人信息
        self.bedCurrent = list()
        # 等待队列
        self.waitingQueue = list()
        for _ in range(len(self.WAITING_QUEUE_TYPE)):
            self.waitingQueue.append(list())
        # 病床历史病人记录
        self.bedHistory = list()
        for _ in range(self.BED_COUNT):
            self.bedCurrent.append(None)
            self.bedHistory.append(list())
        # 优先策略
            # 周一：外伤>老化>白内障单眼>青光眼>视网膜疾病>白内障双眼
            # 周二：外伤>老化>白内障单眼>青光眼>视网膜疾病>白内障双眼
            # 周三：外伤>老化>青光眼>视网膜疾病>白内障双眼>白内障单眼
            # 周四：外伤>老化>青光眼>视网膜疾病>白内障双眼>白内障单眼
            # 周五：外伤>老化>青光眼>视网膜疾病>白内障双眼>白内障单眼
            # 周六：外伤>老化>白内障双眼>白内障单眼>青光眼>视网膜疾病
            # 周日：外伤>老化>白内障双眼>白内障单眼>青光眼>视网膜疾病
        self.PRIORITY = (
            (4, 5, 0, 3, 2, 1),
            (4, 5, 0, 3, 2, 1),
            (4, 5, 3, 2, 1, 0),
            (4, 5, 3, 2, 1, 0),
            (4, 5, 3, 2, 1, 0),
            (4, 5, 1, 0, 3, 2),
            (4, 5, 1, 0, 3, 2)
        )
        # 平均恢复时间（范围再加1天，此处为下限）
        self.recoverTime = (2, 2, 10, 8, 6)
        # 周末是否手术
        self.WORK_ON_WEEKEND = False

        # self.temp = 0

    # 分配床位号
    def allocateBed(self):
        for i in range(len(self.bedCurrent)):
            if self.bedCurrent[i] is None:
                return i
        return None

    # 清退当日出院人员
    def checkout(self):
        # temp = 0
        for i in self.bedCurrent:
            if i is not None and i[6] is not None and i[6] <= self.now:
                self.bedHistory[self.bedCurrent.index(i)].append(i)
                self.changeCountLog[-1] += 1
                self.bedCurrent[self.bedCurrent.index(i)] = None

    # 安排病房

    def checkinIN(self):
        for que in self.waitingQueue:
            deleteList = list()
            for i in que:
                if i[3] == self.now:
                    self.bedCurrent[self.allocateBed()] = deepcopy(i)
                    deleteList.append(que.index(i))
            for i in deleteList[::-1]:
                del(
                    self.waitingQueue[
                        self.waitingQueue.index(que)
                    ][i]
                )
                # self.temp += 1

    # 安排病房

    def checkin(self):
        # temp  = list()
        # for _ in range(6):
        #     temp.append(0)
        for i in self.PRIORITY[self.now.weekday()]:
            que = self.waitingQueue[i]
            # delCount = 0
            while len(que) > 0:
                emptyRoomNumber = self.allocateBed()
                if emptyRoomNumber is None:
                    return
                # 入院
                self.bedCurrent[emptyRoomNumber] = deepcopy(que[0])
                self.bedCurrent[emptyRoomNumber][3] = self.now
                del(que[0])
            #     delCount += 1
            # for _ in range(delCount):
            #     del(que[0])

    # 读入数据表记录

    def recordIN(self):
        while(self.rawData[0][2] <= self.now):
            for i in range(3, 7):
                if self.rawData[0][i] is not None and \
                        self.rawData[0][i] > self.DIVIDED_DATE:
                    self.rawData[0][i] = None
            self.waitingQueue[
                self.WAITING_QUEUE_TYPE.index(
                    self.rawData[0][1]
                )
            ].append(deepcopy(self.rawData[0]))
            del(self.rawData[0])

    # 读入数据表记录

    def record(self):
        while(len(self.rawData) > 0 and self.rawData[0][2] <= self.now):
            self.waitingQueue[
                self.WAITING_QUEUE_TYPE.index(
                    self.rawData[0][1])
            ].append(
                [
                    self.rawData[0][0],
                    self.rawData[0][1],
                    self.rawData[0][2],
                    None,
                    None,
                    None,
                    None
                ]
            )
            del(self.rawData[0])

    # 老化
    def aging(self):
        for que in range(len(self.waitingQueue)-1):
            # 外伤不加入老化队列
            if que == 4:
                continue
            for i in self.waitingQueue[que]:
                if (self.now-i[2]).days > 10:
                    self.waitingQueue[-1].append(deepcopy(i))
                    del(
                        self.waitingQueue[que][
                            self.waitingQueue[que].index(i)
                        ]
                    )
    # 安排手术

    def operation(self):
        for i in self.bedCurrent:
            if i is None:
                continue
            # 未安排手术
            if i[4] is None:
                # 白内障系列
                if i[1] == self.DISEASE[0]:
                    limit = randint(1, 2)
                    delta0 = (7-(i[3]+timedelta(days=limit)).weekday()) % 7
                    delta1 = (9-(i[3]+timedelta(days=limit)).weekday()) % 7
                    delta = min(delta0, delta1)
                    i[4] = i[3]+timedelta(days=delta)
                elif i[1] == self.DISEASE[1]:
                    limit = randint(1, 2)
                    delta = (7-(i[3]+timedelta(days=limit)).weekday()) % 7
                    i[4] = i[3]+timedelta(days=delta)
                    i[5] = i[3]+timedelta(days=delta+2)
                # 外伤
                elif i[1] == self.DISEASE[4]:
                    i[4] = i[3]+timedelta(days=1)
                    if not self.WORK_ON_WEEKEND:
                        if i[4].weekday() == 5:
                            i[4] += timedelta(days=3)
                        elif i[4].weekday() == 6:
                            i[4] += timedelta(days=2)
                # 其他疾病
                else:
                    limit = randint(2, 3)
                    i[4] = i[3]+timedelta(days=limit)
                    if i[4].weekday() == 0 or i[4].weekday() == 2:
                        i[4] += timedelta(days=1)
                    if not self.WORK_ON_WEEKEND:
                        if i[4].weekday() == 5:
                            i[4] += timedelta(days=3)
                        elif i[4].weekday() == 6:
                            i[4] += timedelta(days=2)
    # 术后恢复

    def recover(self):
        for i in self.bedCurrent:
            if i is None:
                continue
            if i[6] is None:
                if i[1] != self.DISEASE[1]:
                    i[6] = i[4]+timedelta(
                        randint(
                            self.recoverTime[
                                self.DISEASE.index(i[1])
                            ],
                            self.recoverTime[
                                self.DISEASE.index(i[1])
                            ]+1
                        )
                    )
                else:
                    i[6] = i[5]+timedelta(
                        randint(
                            self.recoverTime[
                                self.DISEASE.index(i[1])
                            ],
                            self.recoverTime[
                                self.DISEASE.index(i[1])
                            ]+1
                        )
                    )

    # 初始化

    def initialize(self):
        while (self.now - self.DIVIDED_DATE).days < -1:
            self.now += timedelta(days=1)
            # print(self.now, self.WEEKDAY[self.now.weekday()])
            # 换人病床统计数添加计数
            self.changeCountLog.append(0)
            # 清退当日出院人员
            self.checkout()
            # 读入数据表记录
            self.recordIN()
            # 安排住院
            self.checkinIN()
            # print(self.changeCountLog[-1])

    def update(self):
        while self.now <= self.FINISH_DATE:
            self.now += timedelta(days=1)
            # print(self.now)
            # 换人病床统计数添加计数
            self.changeCountLog.append(0)
            # 清退当日出院人员
            self.checkout()
            # 判断老化条件，移动到老化队列
            self.aging()
            # 安排病房
            self.checkin()
            # 安排手术
            self.operation()
            # 术后恢复
            self.recover()
            # 读入数据表记录
            self.record()
            # print(self.WEEKDAY[self.now.weekday()], self.changeCountLog[-1])

    # 评估平均周转时间
    def evaluateTurnover(self):
        sum = 0
        for bed in self.bedHistory:
            for i in bed:
                sum += (i[6]-i[3]).days
        sum = 1/(sum/self.SUM_PATIENT)*5.28
        print('平均周转时间\t', sum)
        return sum

    # 评估准备时间满意度

    def evaluatePrep(self):
        avg = (
            2.38,
            3.63,
            2.37,
            2.42,
            1.00
        )
        sum = 0
        sumSat = 0
        sumList = list()
        conList = list()
        for _ in range(len(self.DISEASE)):
            sumList.append(0)
            conList.append(0)
        for bed in self.bedHistory:
            for i in bed:
                delta = (i[4]-i[3]).days
                res = sigmoid(delta, avg[self.DISEASE.index(i[1])], 4)
                sumSat += res
                sum += delta
                key = self.DISEASE.index(i[1])
                sumList[key] += delta
                conList[key] += 1
        for i in range(len(self.DISEASE)):
            sumList[i] /= conList[i]
        sum /= self.SUM_PATIENT
        sumSat /= self.SUM_PATIENT
        print('平均准备时间\t', sum)
        print('准备时间满意度\t', sumSat)
        for i in range(len(self.DISEASE)):
            print('\t', self.DISEASE[i], '\t', sumList[i])
        return sumSat

    # 评估等待时间满意度
    def evaluateWait(self):
        avg = (
            12.68,
            12.68,
            12.72,
            12.31,
            1.00
        )
        sum = 0
        sumSat = 0
        sumList = list()
        conList = list()
        for _ in range(len(self.DISEASE)):
            sumList.append(0)
            conList.append(0)
        for bed in self.bedHistory:
            for i in bed:
                delta = (i[3]-i[2]).days
                res = sigmoid(delta, avg[self.DISEASE.index(i[1])], 2)
                sumSat += res
                sum += delta
                key = self.DISEASE.index(i[1])
                sumList[key] += delta
                conList[key] += 1
        for i in range(len(self.DISEASE)):
            sumList[i] /= conList[i]
        sum /= self.SUM_PATIENT
        sumSat /= self.SUM_PATIENT
        print('平均等待时间\t', sum)
        print('等待时间满意度\t', sumSat)
        for i in range(len(self.DISEASE)):
            print('\t', self.DISEASE[i], '\t', sumList[i])
        return sumSat

    # 病房使用率
    def bedUsedRate(self):
        usedDays = 0
        totalDays = ((
            self.FINSIH_RATE_DATE -
            self.DIVIDED_DATE
        ).days)*self.BED_COUNT
        for bed in self.bedHistory:
            for i in bed:
                if i[6] < self.DIVIDED_DATE or i[3] > self.FINSIH_RATE_DATE:
                    continue
                else:
                    usedDays += (
                        min(i[6], self.FINSIH_RATE_DATE) -
                        max(i[3], self.DIVIDED_DATE)
                    ).days
                    # 存在同一天某床位同时有人出院入院
                    last = bed.index(i) - 1
                    if last >= 0:
                        if bed[last][6] == i[3]:
                            continue
                        else:
                            usedDays += 1

        res = usedDays/totalDays
        print('统计病房使用\t%f' % res)
        return res

    def test(self):
        self.initialize()
        self.update()
        # print(self.evaluateTurnover())
        # print(self.evaluatePrep())
        # print(self.evaluateWait())
        # count = list()
        # sum = list()
        # for _ in range(len(self.DISEASE)):
        #     count.append(0)
        #     sum.append(0)
        # for bed in self.bedHistory:
        #     for i in bed:
        #         count[self.DISEASE.index(i[1])] += 1
        #         sum[self.DISEASE.index(i[1])] += (i[3]-i[2]).days
        # for i in range(len(self.DISEASE)):
        #     sum[i] /= count[i]
        # print(sum)
        # for bed in self.bedHistory:
        #     for i in bed:
        #         if i[1] == '外伤':
        #             if (i[3]-i[2]).days > 1:
        #                 pass

    # 评分

    def score(self):
        tmp = 0
        tmp += 0.3*self.evaluateTurnover()
        tmp += 0.5*self.evaluateWait()
        tmp += 0.1*self.evaluatePrep()
        tmp += 0.1*self.bedUsedRate()
        print('score%f' % tmp)
        return tmp

# 满意度sigmoid变种函数


def sigmoid(x: float, b: float, k: float)->float:
    return -1/(1+E**(k*(-x+b)))+1


if __name__ == '__main__':
    # inpatientSystem = InpatientSystem()
    # inpatientSystem.test()
    scoreList = list()
    x = list(range(0, 31))
    for i in range(0, 31):
        print('=====Aging %d=====' % i)
        inpatientSystem = InpatientSystem()
        inpatientSystem.AGING_JUDGING = i
        inpatientSystem.test()
        scoreList.append(inpatientSystem.score())
    for i in range(len(x)):
        print(x[i], scoreList[i])
    pass
