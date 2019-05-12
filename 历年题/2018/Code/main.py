from CNC import CNC
from RGV import RGV
from Res import Res
from inheritance import Item
NO = 0  # 组号[0:2]
NUM = 1 # 题目号[1:3]
rgv = None
machineList = None
timeTable = []
res = Res(NO,NUM)
output = 0
clockSum  = 0
def goAlong(route:list)->int:
    for i in route:
        goto(machineList[i])
        if clockSum > 8 * 3600:
            return output-1
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
        # print('cnc %d finished %d th work at clock %d'% (cnc.id,output,clockSum))
        timeTable[cnc.id]=clockSum+res.getProcessTime()
    else:
        pass

def snap():
    global clockSum
    u=""
    d=""
    for i in range(8):
         if i%2==0:
            u+=str(timeTable[i])+'\t'
         else:
            d+=str(timeTable[i])+'\t'
    print('=================================\n'+u)
    for i in range(int(rgv.position)):
        print('\t',end='',sep='')
    print('[==]')
    print(d+'\n=================================\n')

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
    exp = Item()
    print(goAlong(exp.alignment))


