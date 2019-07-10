from datetime import datetime, timedelta
from dataReader import dataReader


class InpatientSystem:
    def __init__(self):
        # 数据表中数据
        self.rawData = dataReader()[0]
        # 开始日期基准点
        self.INITIAL_DATE = datetime(2008, 6, 30)
        # 更换策略日期
        self.DIVIDED_DATE = datetime(2008, 8, 8)
        self.WEEKDAY = ('周一', '周二', '周三', '周四', '周五', '周六', '周日')
        # 床位数
        self.BED_COUNT = 79
        # 今日日期
        self.now = self.INITIAL_DATE
        # 每日换人病床统计数
        self.changeCountLog = list()
        # 当前病床病人信息
        self.bedCurrent = list()
        # 病床历史病人记录
        self.bedHistory = list()
        for _ in range(self.BED_COUNT):
            self.bedCurrent.append(None)
            self.bedHistory.append(None)

    def initialize(self):
        while self.now <= self.DIVIDED_DATE:
            self.now += timedelta(days=1)
            # 换人病床统计数添加计数
            self.changeCountLog.append(0)
            # 清退当日出院人员
            for i in self.bedCurrent:
                if i != None and i.leaveTime == self.now:
                    self.bedHistory[self.bedCurrent.index(i)].append(i)
                    self.changeCountLog[-1] += 1
                    i = None
            # 读入数据表记录
            while(self.rawData[0][2]<=self.now):
                for i in self.rawData[0]:
                    if i>self.DIVIDED_DATE:
                        i = None
            print(self.now, self.WEEKDAY[self.now.weekday()])

    def test(self):
        self.initialize()


if __name__ == '__main__':
    inpatientSystem = InpatientSystem()
    inpatientSystem.test()
