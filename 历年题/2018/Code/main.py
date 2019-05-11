from CNC import CNC
from RGV import RGV
from Res import Res
NO = 0  # 组号[0:2]
NUM = 1 # 题目号[1:3]
rgv = None
machineList = None
timeTable = []
res = Res(NO,NUM)
output = 0
clockSum  = 0
def goAlong():
    pass
def initialGoAlong():
    for i in range(8):
        goto(machineList[i])
    # for test
    for i in range(80):
        for i in range(8):
            goto(machineList[i])
def goto(cnc: CNC):
    assert cnc is not None
    global clockSum
    global output
    rgv.position = cnc.position
    clockSum += res.getDistenceTime(rgv,cnc)
    if timeTable[cnc.id]==None:
        timeTable[cnc.id]=clockSum+res.getProcessTime()
    elif clockSum>timeTable[cnc.id]:
        wash()
        print('cnc %d finished %d th work at clock %d'% (cnc.id,output,clockSum))
        timeTable[cnc.id]=clockSum+res.getProcessTime()
    else:
        pass

   
def wash():
    global clockSum
    global output
    clockSum += res.getWashTime()
    output+=1


if __name__ == '__main__':
    clockSum = 0
    machineList = []
    timeTable = []
    for i in range(8):
        machineList.append(CNC(i))
        timeTable.append(None)
    rgv = RGV()
    initialGoAlong()

