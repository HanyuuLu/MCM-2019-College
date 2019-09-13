import time
import datetime

class Conf:
    def __init__(self) -> dict:
        '''
        # 参数获取
        - fareAvg 平均打车费
        - lanes 车道数
        - initialTexi 初始出租车数量
        - disCenter 正太中心点
        - disRight 正太右5%点
        - taxiAvgPeople 平均出租车单次载人数
        - planeRate 飞机上座率
        - initDate 起始日期
        '''
        self.fareAvg = 100
        self.lanes = 1
        self.initialTaxi = 120
        self.disCenter = 120
        self.disRight = 60
        self.taxiRate = 0.15
        self.taxiAvgPeople = 1.3
        self.planeRate = 0.8
        self.initDate = datetime.datetime.strptime("2019-09-12", "%Y-%m-%d")


if __name__ == '__main__':
    conf = Conf()
    print(conf.initDate)
