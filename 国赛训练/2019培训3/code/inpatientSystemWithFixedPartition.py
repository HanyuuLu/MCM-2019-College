from copy import deepcopy
from datetime import datetime, timedelta
from math import e as E
from random import randint
from statistics import Const

from dataReader import dataReader
from inpatientSystem import InpatientSystem


class InpatientSystemWithFixedParition(InpatientSystem):
    def __init__(self):
        super().__init__()
        self.PARTITION = [15, 20, 9, 25, 10]

    # 分配床位号
    def allocateBedSP(self, tp: int):
        assert tp in [0, 1, 2, 3, 4], "[ERROR}非法下标访问"
        lowerLimit = sum(self.PARTITION[:tp])
        higherLimit = lowerLimit + self.PARTITION[tp]
        pass
        for x in range(lowerLimit, higherLimit):
            if self.bedCurrent[x] is None:
                return x
        return None

    # 安排病房
    def checkin(self):
        # for i in self.PRIORITY[self.now.weekday()]:
        #     que = self.waitingQueue[i]
        #     # delCount = 0
        #     while len(que) > 0:
        #         emptyRoomNumber = self.allocateBed()
        #         if emptyRoomNumber is None:
        #             return
        #         # 入院
        #         self.bedCurrent[emptyRoomNumber] = deepcopy(que[0])
        #         self.bedCurrent[emptyRoomNumber][3] = self.now
        #         del(que[0])
        for que in self.waitingQueue:
            delCount = 0
            for i in que:
                key = self.allocateBedSP(self.waitingQueue.index(que))
                if key is None:
                    break
                self.bedCurrent[key] = deepcopy(i)
                self.bedCurrent[key][3]=self.now
                delCount += 1
            for i in range(delCount)[::-1]:
                del(que[i])

    def update(self):
        while self.now <= self.FINISH_DATE:
            self.now += timedelta(days=1)
            # print(self.now)
            # 换人病床统计数添加计数
            self.changeCountLog.append(0)
            # 清退当日出院人员
            self.checkout()
            # # 判断老化条件，移动到老化队列
            # self.aging()
            # 安排病房
            self.checkin()
            # 安排手术
            self.operation()
            # 术后恢复
            self.recover()
            # 读入数据表记录
            self.record()
            # print(self.WEEKDAY[self.now.weekday()], self.changeCountLog[-1])

    def test(self):
        self.initialize()
        self.update()


if __name__ == '__main__':
    # inpatientSystem = InpatientSystem()
    # inpatientSystem.test()
    inpatientSYstem = InpatientSystemWithFixedParition()
    inpatientSYstem.test()
    inpatientSYstem.score()
    # scoreList = list()
    # x = list(range(0, 31))
    # for i in range(0, 31):
    #     print('=====Aging %d=====' % i)
    #     inpatientSystem = InpatientSystem()
    #     inpatientSystem.AGING_JUDGING = i
    #     inpatientSystem.test()
    #     scoreList.append(inpatientSystem.score())
    # for i in range(len(x)):
    #     print(x[i], scoreList[i])
    # pass
