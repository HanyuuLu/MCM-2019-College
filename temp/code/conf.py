import datetime


class Conf:
    def __init__(self) -> dict:
        '''
        # 参数获取
        - fareAvg 平均打车费
        - lanes 车道数
        - initialTexi 初始出租车数量
        - disRight 正态右边界
        - disLeft 正态左边界
        - miu 正态参数
        - sigma 正态参数
        - taxiAvgPeople 平均出租车单次载人数
        - planeRate 飞机上座率
        - initDate 起始日期
        - departRate 出发乘客使用出租车比例
        - arriveRate 到达乘客使用出租车比例
        - defaultWaitTime 推荐司机等待时间
        '''
        self.fareAvg = 100
        self.lanes = 2
        self.vLanes = 5
        self.patch = self.lanes*self.vLanes
        self.initialTaxi = 0
        self.departRight = -60
        self.departLeft = -180
        self.departMiu = -120
        self.departSigma = 30.6122
        self.arriveLRight = 40
        self.arriveLLeft = 20
        self.arriveLMiu = 30
        self.arriveLSigma = 3.054
        self.arriveHRight = 55
        self.arriveHLeft = 29
        self.arriveHMiu = 42
        self.arriveHSigma = 5.102
        self.arriveLRate = 0.7
        self.taxiRate = 0.15
        self.taxiAvgPeople = 1.3
        self.planeRate = 0.8
        self.initDate = datetime.datetime.strptime("2019-09-12", "%Y-%m-%d")
        self.departRate = 0.1356
        self.arriveRate = 0.1
        self.processTime = \
            {
                "depart2choice": 5,
                "waitPassenger": 1,
            }
        self.startDate = datetime.datetime(2019, 9, 12)
        self.endDate = datetime.datetime(2019, 9, 14)
        self.maxWaitTime = 1800
        self.maxWaitingQueue = 300
        self.defaultWaitTime = 132
        self.averageProfits = 50
        self.averageCash = 110
        self.toCity = 45
        self.clipWindowDepartLeft = 90
        self.clipWindowDepartRight = 120
        self.clipWindowArriveLeft = -45
        self.clipWindowArriveRight = -15
        


if __name__ == '__main__':
    conf = Conf()
    print(conf. startDate)
