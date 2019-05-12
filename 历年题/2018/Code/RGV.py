from CNC import CNC
from Res import Res
class RGV:
    def __init__(self,no,num):
        self.position = 0		# 当前位置
        self.no = no    # 组号[0:2]
        self.num = num  #题目号[1:3]
        self.machineList = []
        self.timeTable = []
        self.res = Res(self.no, self.num)
        self.output = 0
        self.clock = 0
        for i in range(self.res.machineNumber):
            self.timeTable.append(None)
            self.machineList.append(CNC(i))

    def goto(self, cncID: int):
        assert cncID>=0 and cncID<self.res.machineNumber,"cncID: %d 超出可接受范围"%cncID
        self.clock += self.res.getDistenceTime(abs(self.position - int(cncID / 2)))
        # print(self.clock)
        self.position = int(cncID/2)
        if self.timeTable[cncID] == None:
            self.timeTable[cncID] = self.clock+self.res.getProcessTime()
        elif self.clock > self.timeTable[cncID]:
            self.clock += self.res.getWashTime()
            self.output += 1
            self.timeTable[cncID] = self.clock + self.res.getProcessTime()
            # print("cncID %d output %d"%(cncID,self.output))
        else:
            pass
    def goAlong(self,route: list) -> int:
        for i in route:
            self.goto(i)
            if self.clock > self.res.timeUpBound:
                self.output -= 1
                return (self.output, True)
        return (self.output, False)
