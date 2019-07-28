# for issue 49
import os
import sys
import gc
sys.path.append('.\\')
from copy import deepcopy
from json import dump
from math import e

from core.const import OUTPUT_PATH
from core.dataReader import dataReader, dataReader2
from core.longitudeAndLatitudeConverter import lalConverter

# 挑选阈值
SELECT_THRESHOLDS = 0.05
# 接受阈值
FINISH_THRESHOLDS = 0.06460243463516235
# 价差门槛
DELTA_THRESHOLDS = 60


def distance(obj1: list, obj2: list):
    assert isinstance(obj1, list) or isinstance(obj1, tuple), \
        '[ERROR] 第一个参数应当为list或者tuple,输入的参数类型为%s' % str(type(obj1))
    assert isinstance(obj2, list) or isinstance(obj2, tuple), \
        '[ERROR] 第二个参数应当为list或者tuple,输入的参数类型为%s' % str(type(obj2))
    return ((obj1[0] - obj2[0]) ** 2 + (obj1[1] - obj2[1]) ** 2)**0.5


class Calc:
    r'''
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
        finished = 0
        res = list()
        # 会员按照上述顺序排队，依次预定任务
        self.memberList.sort(key=lambda x: (x.startTime, -x.reputation))
        avilableList = deepcopy(self.taskList)
        del(self.taskList)
        for member in self.memberList:
            if hasattr(member, 'orderList'):
                del(member.orderList)
            member.orderList = list()
            for i in avilableList:
                dis = distance(i.position, member.position)
                i.prop = i.pricePremiumNormalize * \
                    i.weight['premium'] + e**- \
                    distance(i.position, member.position) * \
                    i.weight['distance']
            avilableList.sort(key=lambda x: -x.prop)
            while len(member.orderList) < member.maxOrder and len(avilableList) > 0 and avilableList[0].prop > SELECT_THRESHOLDS:
                member.orderList.append(avilableList[0])
                avilableList.remove(avilableList[0])
            for order in member.orderList:
                order.finished = order.prop - 1 / member.reputation - FINISH_THRESHOLDS > 0
            finished += sum([x.finished for x in member.orderList])
            res.append({
                'no': member.no,
                'reputation': member.reputation,
                'position': member.position,
                'start time': str(member.startTime),
                'selected': len(member.orderList),
                'finished': sum([x.finished for x in member.orderList]),
                'remain': len(avilableList),
            })
        self.unlinkedTaskList = avilableList
        fileName = os.path.join(OUTPUT_PATH, 'issue49.json')
        with open(fileName, 'w') as w:
            dump(res, w)
        self.debug()
        return finished


    def debug(self):
        finished = 0
        total = 0
        for member in self.memberList:
            for order in member.orderList:
                total += 1
                if order.finished:
                    finished += 1
        for order in self.unlinkedTaskList:
            total += 1
        print('%f/%f'%(finished,total))


    def dev(self):
        ''' # issue 50
- 根据Excel表中的原定价方案 计算出已完成任务的预期最低定价 从而计算出多出的资金 并且根据新的任务定价方案 得出现在会员的任务分配
- 根据现有的任务分配方案计算出未完成任务的差价，对差价按照升序进行排序，并且设置差价门槛。按照差价的排序，给未完成任务提高定价。资金花完或者当前差价大于差价门槛时就结束，从而得出新的定价方案。 按照新的方案得出任务完成率以及完成（不考虑未完成）
- 调整差价的门槛，计算满意程度（-0.6*当前成本/原方案成本+任务完成率），最优化使得满意程度最大

        '''

        self.calc()
        self.origCost = 0
        for member in self.memberList:
            for order in member.orderList:
                self.origCost += order.priceBase + order.pricePremium
        for order in self.unlinkedTaskList:
            self.origCost += order.priceBase + order.pricePremium

        taskList = list()
        # 结余资金
        # 扣除完成任务多余投入
        self.restfulPrice = 0
        for member in self.memberList:
            for order in member.orderList:
                if order.finished:
                    toPrice = round(order.priceBase / order.weight['premium'] * (
                        FINISH_THRESHOLDS + 1 / member.reputation - e ** (-distance(
                            member.position,order.position
                        ))*order.weight['distance']
                    ),2)
                    if toPrice < 0:
                        toPrice = 0
                    assert order.pricePremium >= toPrice
                    # 抽钱补款
                    self.restfulPrice += order.pricePremium - toPrice
                    order.pricePremium = toPrice
            taskList.extend(member.orderList)
        self.taskList = taskList
        self.taskList.extend(self.unlinkedTaskList)
        print('$%f saved' % self.restfulPrice)
        self.origRestfulPrice = self.restfulPrice
        gc.collect()
        self.calc()
        self.newTasklist = list()
        self.newTasklist.extend(self.unlinkedTaskList)
        # 补贴未完成任务投入
        for member in self.memberList:
            for order in member.orderList:
                if hasattr(order,'finished') and not order.finished:
                    toPrice = round((FINISH_THRESHOLDS + 1 / member.reputation - order.weight['distance']*e**(-distance(
                        member.position, order.position))) / order.weight['premium'] * order.priceBase,2)
                    assert toPrice>0
                    order.priceDelta = -order.pricePremium + toPrice
                    assert order.priceDelta >= 0
                    order.pricePremium = toPrice
            self.newTasklist.extend(member.orderList)
        self.sortByIssue50()
        flag = True
        for task in self.taskList:
            if flag:
                '''
                当资金充足、下一个任务未完成且需要提升的价格低于提升意愿门槛时，提升任务的价格至预期预期完成线
                '''
                if not hasattr(task,'finished')  or task.finished or self.restfulPrice < task.priceDelta or task.priceDelta>DELTA_THRESHOLDS:
                    flag = False
                self.restfulPrice -= task.priceDelta
                task.pricePremium += task.priceDelta
            else:
                '''
                上述条件破裂后，将剩余任务溢价全部调整为0以降低成本
                '''
                self.restfulPrice+=task.pricePremium
                task.pricePremium = 0
        gc.collect()
        self.calc()
        self.newTasklist = list()
        self.newTasklist.extend(self.unlinkedTaskList)
        for member in self.memberList:
            self.newTasklist.extend(member.orderList)
        self.sortByIssue50()
        '''
        满意程度（-0.6*当前成本/原方案成本+任务完成率）
        * 成本计算是所有任务（包括完成未完成和未挑选的任务）的标示价格
        * 任务完成率是完成任务占总任务的比例
        '''
        cost = 0
        finishedCount = 0
        for task in self.taskList:
            if hasattr(task,'finished') and task.finished:
                finishedCount += 1
            cost += task.pricePremium + task.priceBase
        scoreCost = cost / self.origCost
        scoreFinRate = finishedCount / len(self.taskList)
        score = -0.6 * scoreCost + scoreFinRate * 0.4
        print('%f devoted to unfinished'%(self.origRestfulPrice-self.restfulPrice))
        print('%f$ left' % self.restfulPrice)
        print('cost\t%f' % scoreCost)
        print('finishRate\t%f' % scoreFinRate)
        print('score\t%f' % score)


    def sortByIssue50(self):
        ''' # Issue中对任务排序
        1. 未完成任务
        2. 未挑选任务
        3. 已完成任务
        self.newTaskList -> self.taskList
        '''
        self.taskList = list()
        gc.collect()
        # 未完成任务
        for x in self.newTasklist[:]:
            if hasattr(x, 'finished') and not x.finished:
                self.taskList.append(x)
                self.newTasklist.remove(x)
        self.taskList.sort(key=lambda x: x.priceDelta)
        # 未挑选任务
        for x in self.newTasklist[:]:
            if not hasattr(x, 'finished'):
                self.taskList.append(x)
                self.newTasklist.remove(x)
        # 已完成任务
        for x in self.newTasklist[:]:
            self.taskList.append(x)
            self.newTasklist.remove(x)
        del(self.newTasklist)
        gc.collect()


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
 - startTime: 开始时间
 - maxOrder: 最大限额
 '''

    def __init__(self, *args):
        args = args[0]
        self.no = args[0]
        self.reputation = args[4]
        self.position = lalConverter(args[1])
        self.startTime = args[3]
        self.maxOrder = args[2]


if __name__ == '__main__':
    calc = Calc()
    calc.dev()
    # l = 0
    # r = 1
    # key = 522
    # while True:
    #     FINISH_THRESHOLDS = (l + r) / 2
    #     res = calc.calc()
    #     print(FINISH_THRESHOLDS,'\t', res)
    #     if res > key:
    #         l = (l + r) / 2
    #     elif res < key:
    #         r = (l + r) / 2
    #     else:
    #         break

    pass
