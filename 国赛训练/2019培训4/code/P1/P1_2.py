# for issue 49
import sys
from  copy import deepcopy
sys.path.append('.\\')
from math import e
from core.dataReader import dataReader, dataReader2
from core.longitudeAndLatitudeConverter import lalConverter


def distance(obj1: list, obj2: list):
    assert isinstance(obj1, list) or isinstance(obj1, tuple), \
        '[ERROR] 第一个参数应当为list或者tuple,输入的参数类型为%s' % str(type(obj1))
    assert isinstance(obj2, list) or isinstance(obj2, tuple), \
        '[ERROR] 第二个参数应当为list或者tuple,输入的参数类型为%s' % str(type(obj2))
    return ((obj1[0] - obj2[0]) ** 2 + (obj1[1] - obj2[1]) ** 2)**0.5


class Calc:
    '''
    # 任务定价方案
## 会员
 - reputation:信誉度
 - position:坐标

## 任务
- parameters
  - position:坐标(单位，0起点的公里数)
  - priceBase:任务基本价
  - pricePremium:任务溢价
  - pricePremiumNormalize:归一化之后的任务溢价
  - priceRatio:价格吸引度
  - weight:权重
    - premium:任务溢价
    - distance:任务距离
## 计算
  - $distanceNormalize = \frac{1}{e^distance(task.distance,member.distance)}$
  - $priceRatio = \frac{pricePremium}{priceBase}$:归一化
  - $prop = pricePremiumNormailze \times weight.premium + distaceNormalize \times weight.distance$ :
  - $acceptRate = prop - member.reputation$
'''

    def __init__(self):
        self.recData = dataReader()[0]
        self.memData = dataReader2()
        self.taskList = list()
        self.memberList = list()
        for i in self.recData:
            self.taskList.append(Task(i))
        for i in self.memData:
            self.memberList.append(Member(i))
        pass

    def calc(self):
        '''
        主序：时间非降序
        次序：信誉度降序
        '''
        dbg = str()
        self.memberList.sort(key=lambda x: (x.startTime, -x.reputation))
        avilableList = deepcopy(self.taskList)
        for member in self.memberList:
            member.orderList = list()
            for i in avilableList:
                dis = distance(i.position, member.position)
                i.prop = i.pricePremiumNormalize * i.weight['premium'] + e**-distance(i.position,member.position) * i.weight['distance']
            avilableList.sort(key=lambda x: -x.prop)
            while len(member.orderList) <= member.reputation and len(avilableList)>0 and avilableList[0].prop>0.05:
                member.orderList.append(avilableList[0])
                avilableList.remove(member.orderList[-1])
            dbg += '%d\t%d\n' % (len(member.orderList), len(avilableList))
            with open('debug.log','w+') as w:
                w.write(dbg)


    pass


class Task:
    '''
    ## 任务
- parameters
  - position:坐标(单位，0起点的公里数)
  - priceBase:任务基本价
  - pricePremium:任务溢价
  - pricePremiumNormalize:归一化之后的任务溢价
  - priceRatio:价格吸引度
  - weight:权重
    - premium:任务溢价
    - distance:任务距离
'''

    def __init__(self, *args):
        args = args[0]
        self.no = args[0]
        self.position = lalConverter((args[1], args[2]))
        self.priceBase = 65
        self.pricePremium = args[3] - self.priceBase
        self.pricePremiumNormalize = self.pricePremium / self.priceBase
        self.priceRatio = self.pricePremium / self.priceBase
        self.weight = {'premium': 0.6, 'distance': 0.4}


class Member:
    '''
    ## 会员
 - reputation: 信誉度
 - position: 坐标
 '''

    def __init__(self, *args):
        args = args[0]
        self.reputation = args[4]
        self.position = lalConverter(args[1])
        self.startTime = args[3]


if __name__ == '__main__':
    calc = Calc()
    calc.calc()
    pass
