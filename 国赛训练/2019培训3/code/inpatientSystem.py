from datetime import datetime, timedelta
from dataReader import dataReader
from statistics import Const
from copy import deepcopy
from random import randint


class InpatientSystem(Const):
    def __init__(self):
        super().__init__()
        # 数据表中数据
        self.rawData = dataReader()[0]
        # 开始日期基准点
        self.INITIAL_DATE = datetime(2008, 6, 30)
        # 更换策略日期
        self.DIVIDED_DATE = datetime(2008, 8, 8)
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

        self.temp = 0

    # 分配床位号
    def allocateBed(self):
        for i in range(len(self.bedCurrent)):
            if self.bedCurrent[i] == None:
                return i
        return None

    # 清退当日出院人员
    def checkout(self):
        temp = 0
        for i in self.bedCurrent:
            if i != None and i[6]!=None and i[6] <= self.now:
                self.bedHistory[self.bedCurrent.index(i)].append(i)
                self.changeCountLog[-1] += 1
                self.bedCurrent[self.bedCurrent.index(i)] = None
                temp+=1
        print('每日清退人数%d'%temp)

    # 安排病房

    def checkinIN(self):
        for que in self.waitingQueue:
            for i in que:
                if i[3] == self.now:
                    self.bedCurrent[self.allocateBed()] = deepcopy(i)
                    del(
                        self.waitingQueue[
                            self.waitingQueue.index(que)
                        ][
                            que.index(i)
                        ]
                    )
                    self.temp += 1

    # 安排病房

    def checkin(self):
        temp  = list()
        for _ in range(6):
            temp.append(0)
        for i in self.PRIORITY[self.now.weekday()]:
            que = self.waitingQueue[i]
            while len(que) > 0:
                emptyRoomNumber = self.allocateBed()
                if emptyRoomNumber == None:
                    # 没有空床位
                    print('满')
                    print(temp)
                    return
                # 入院
                self.bedCurrent[emptyRoomNumber] = deepcopy(que[0])
                self.bedCurrent[emptyRoomNumber][3] = self.now
                del(que[0])
                temp[i]+=1
                self.temp += 1


    # 读入数据表记录

    def recordIN(self):
        while(self.rawData[0][2] <= self.now):
            for i in range(3, 7):
                if self.rawData[0][i] != None and self.rawData[0][i] > self.DIVIDED_DATE:
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
            if i==None:
                continue
            # 未安排手术
            if i[4] == None:
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
                # 其他疾病
                else:
                    limit = randint(2, 3)
                    i[4] = i[3]+timedelta(days=limit)
                    if i[4].weekday() == 0 or i[4].weekday() == 2:
                        i[4] += timedelta(days=1)
    # 术后恢复

    def recover(self):
        for i in self.bedCurrent:
            if i ==None:
                continue
            if i[6] == None:
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
        while self.now <= self.DIVIDED_DATE:
            self.now += timedelta(days=1)
            # 换人病床统计数添加计数
            self.changeCountLog.append(0)
            # 清退当日出院人员
            self.checkout()
            # 读入数据表记录
            self.recordIN()
            # 安排住院
            self.checkinIN()
            print(
                self.now, self.WEEKDAY[self.now.weekday()], self.changeCountLog[-1])

    def update(self):
        while self.now <= self.FINISH_DATE:
            self.now += timedelta(days=1)
            # 换人病床统计数添加计数
            self.changeCountLog.append(0)
            # 清退当日出院人员
            self.checkout()
            # 读入数据表记录
            self.record()
            # 判断老化条件，移动到老化队列
            self.aging()
            # 安排病房
            self.checkin()
            # 安排手术
            self.operation()
            # 术后恢复
            self.recover()
            print(
                self.now, self.WEEKDAY[self.now.weekday()], self.changeCountLog[-1])

    def test(self):
        self.initialize()
        self.update()


if __name__ == '__main__':
    inpatientSystem = InpatientSystem()
    inpatientSystem.test()
    print(inpatientSystem.temp)
    pass
