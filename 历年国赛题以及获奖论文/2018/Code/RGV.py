from CNC import CNC
from Res import Res
import copy
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

    def goto(self, cncID: int)->bool:
        assert cncID>=0 and cncID<self.res.machineNumber,"cncID: %d 超出可接受范围"%cncID
        self.clock += self.res.getDistenceTime(abs(self.position - int(cncID / 2)))
        # print(self.clock)
        self.position = int(cncID/2)
        # cnc无料，上料
        if self.timeTable[cncID] == None:
            self.clock+=self.res.getSwapTime(cncID)
            self.timeTable[cncID] = self.clock+self.res.getProcessTime()
            if self.clock<self.res.timeUpBound:
                return True
            else:
                raise Exception("finish")
                return False
        # cnc已完成，换料，清洗
        elif self.clock >= self.timeTable[cncID]:
            self.clock += self.res.getWashTime()
            self.timeTable[cncID] = self.clock + self.res.getProcessTime()
            if self.clock<self.res.timeUpBound:
                self.output += 1
                return True
            else:
                raise Exception("finish")
                return False
            # print("cncID %d output %d"%(cncID,self.output))
        # cnc加工中，不进行操作
        else:
            if self.clock<self.res.timeUpBound:
                return True
            else:
                raise Exception("finish")
                return False
    def goAlong(self,route: list) -> int:
        for i in route:
            self.goto(i)
            if self.clock > self.res.timeUpBound:
                self.output -= 1
                return (self.output, True)
        return (self.output, False)
    # 直接寻找法
    def intelligenceGoAlong(self):
        while True:
            posNone = []
            try:
                while True:
                    if len(posNone) ==0:
                        posNone.append(self.timeTable.index(None))
                    else:
                        posNone.append(self.timeTable.index(None,posNone[-1]+1))
            except Exception as e:
                pass
            if len(posNone) !=0:
                for i in posNone:
                    try:
                        self.goto(i)
                        print(self.output)
                    except Exception as e:
                        return self.output
            else:
                next = self.timeTable.index(min(self.timeTable))
                try:
                    self.clock = min(self.timeTable)
                    self.goto(next)
                    print(self.output)
                except Exception as e:
                    return self.output

# 周期法

count = 0
upperBound = None            
# 上界预估函数
def initialUperBound()->int:
    rgv = RGV(0,1)
    for i in range(rgv.res.machineNumber):
        rgv.goto(i)
    return max(rgv.clock,min(rgv.timeTable))

def cal(avilableList:list,rgv:RGV)->int:
    place = []
    for i in avilableList:
        place.append(int(i/2))
    set(place)
    place.sort()
    aRgv = copy.deepcopy(rgv)
    bRgv = copy.deepcopy(rgv)
    for i in place:
        aRgv.goto(i)
    place.reverse()
    for i in place:
        bRgv.goto(i)
    res = min(aRgv,bRgv,key= lambda x:x.clock)
    for i in avilableList:
        res.clock+=rgv.res.getSwapTime(i)
    return res.clock
def turn(avilableList:list,rgv:RGV)->RGV:
    global count,upperBound
    count +=1
    # print(count,'\t',avilableList)
    rgvList = []
    avlList = []
    if len(avilableList) == 0:
        assert isinstance(rgv,RGV)
        upperBound = min(upperBound,rgv.clock)
        return rgv
    if cal(avilableList,rgv)>upperBound:
        nan = copy.deepcopy(rgv)
        nan.clock = float('inf')
        return nan
    for i in avilableList:
        temp =copy.deepcopy(avilableList)
        temp.remove(i)
        avlList.append(temp)
        rgvList.append(copy.deepcopy(rgv))
        assert isinstance(rgvList[0],RGV)
        rgvList[-1].goto(i)
        rgvList[-1] = (turn(avlList[-1],rgvList[-1]))
        assert isinstance(rgvList[0],RGV)
    return rgvList[rgvList.index(min(rgvList,key=lambda x:x.clock))]
    
        
# 周期法
def rurnaround(rgv:RGV):
    global upperBound 
    upperBound = initialUperBound()
    avilableList = []
    for i in range(rgv.res.machineNumber):
        avilableList.append(i)
    return turn(avilableList,rgv).clock


if __name__=='__main__':
    rgv = RGV(0,1)
    # print(rgv.intelligenceGoAlong())
    print(rurnaround(rgv))
    # print(initialUperBound())


