# from RGV import RGV
from CNC import CNC

class Res:
    def __init__(self, no, num):
        # 分组号
        self.no = no
        # 问题序号
        self.num = num
        # 加工时间表
        # 0:加工完成一道工序所用的物料所需时间
        # 1:加工完成两道工序第一道工序所用的物料所需时间
        # 2:加工完成两道工序第二道工序所用的物料所需时间
        self.processTimeTable = \
            [[560, 400, 378],
                [580, 280, 500],
                [545, 455, 182]]
        #上下料时间表
        self.swapTimeTable = \
            [[28, 31],
                [30, 35],
                [27, 32]]
        # 距离表
        self.distenceTable = \
            [[0,20, 33, 46],
                [0,23, 41, 59],
                [0,18, 32, 46]]
        # 清洗时间表
        self.washTimeTable = \
            [25,
                30,
                25]
        self.timeUpBound = 8 * 3600
        self.machineNumber = 8
    # 获取加工时间
    def getProcessTime(self, *select):
        if len(select) == 0:
            assert self.num == 1  # 仅第一题适用
            return self.processTimeTable[self.no][0]
        elif len(select) == 1:
            assert self.num == 2 or self.num == 3  # 第二题和第三题使用
            assert select[0] > 0 and select[0] < 3  # 只能选择第一步或第二步
            return self.processTimeTable[self.no][select[0]]
        else:
            raise Exception('参数过多')
    # 获取装卸/货时间
    def getSwapTime(self, cnc: CNC):
        return self.swapTimeTable[self.no][1 - cnc.id % 2]
    # 获取行进时间
    # def getDistenceTime(self, rgv: RGV, cnc: CNC):
    #     return self.distenceTable[self.no][abs(rgv.position - cnc.position)]
    # 通过距离获取行进时间
    def getDistenceTime(self, num: int) -> int:
        return self.distenceTable[self.no][num]
    # 获取清洗时间
    def getWashTime(self):
        return self.washTimeTable[self.no]


if __name__ == "__main__":
    res = Res(0, 2)
    print(res.getProcessTime(1))
    cnc = CNC(5)
    print(res.getSwapTime(cnc))
