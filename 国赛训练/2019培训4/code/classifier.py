from math import sqrt
from random import randint, random

import matplotlib.pyplot as plt

from dataReader import dataReader


class Classifier:
    # 初始化、读入数据库、标定数据范围
    def __init__(self):
        # 原始数据
        self.rawData = dataReader()[0]
        # 下标下限
        self.LOWER_LIMIT = 0
        # 下标上限
        self.UPPER_LIMIT = len(self.rawData) - 1

    # 产生一组不重复的随机中心
    def generateRandomCenter(self, typeCount: int):
        # 随机中心（聚类）数
        self.typeCount = typeCount
        # 随机中心编号列表
        self.coreList = list()
        while len(self.coreList) < self.typeCount:
            key = randint(self.LOWER_LIMIT, self.UPPER_LIMIT)
            if key in self.coreList:
                continue
            self.coreList.append(key)
        # print('[center]%s' % str(self.coreList))

    # 聚类计算
    def calc(self):
        # 聚类列表
        self.classList = [list() for _ in range(self.typeCount)]
        for i in self.rawData:
            key = float('inf')
            ptr = -1
            for j in self.coreList:
                distance = dis(i, self.rawData[j])
                if key > distance:
                    ptr = self.coreList.index(j)
                    key = distance
            self.classList[ptr].append(i)
        # print('[info] calc finished 😂')

    # 绘制聚类图
    def draw(self):
        plt.figure()
        plt.title(
            '%d centers with average distance %.4f'
            % (self.typeCount, self.totalAverage)
        )
        # print(str(self.coreList))
        for i in self.classList:
            col = (random(), random(), random())
            plt.plot([x[2] for x in i], [x[1] for x in i],
                     'x', color=col)
        plt.text(112.74, 23.8, str(self.coreList), ha='left', fontsize=8)
        plt.draw()
        # plt.show()
        # plt.text(4, 1, t, ha='left', rotation=15, wrap=True)
        plt.savefig('resPic\%s.jpg' % str(self.typeCount))

    # 计算得分（平均距离）
    def score(self):
        # 每个分组的平均距离
        self.averageList = list()
        try:
            for key in range((len(self.coreList))):
                self.averageList.append(
                    sum([dis(x, self.rawData[self.coreList[key]])
                         for x in self.classList[key]]) /
                    len(self.classList[key])
                )
        except Exception:
            Exception("bad center!")
        # print('[average]')
        self.totalAverage = 0
        # 加权平均
        for i in self.averageList:
            self.totalAverage +=  \
                i*len(self.classList[self.averageList.index(i)])
            # print('\t[group %d]\t%f' % (self.averageList.index(i), i))
        self.totalAverage /= len(self.rawData)
        # print('\t[total]\t\t%f' % self.totalAverage)
        return self.totalAverage

    # 单次运行
    def run(self):
        self.generateRandomCenter(10)
        self.calc()
        self.score()

    # 给定聚类数多次随机取表现较好值
    def des(self, typeCount: int):
        # 最优结果、得分暂存变量
        score = float('inf')
        resList = None
        # 连续conn次没有得到更优化的结果的次数
        conn = 0
        # 尝试次数计数器
        counter = 0
        while (conn < 100):
            counter += 1
            # print('[attempt %d with %d times better]' % (counter, conn))
            self.generateRandomCenter(typeCount)
            self.calc()
            try:
                tempScore = self.score()
            except Exception:
                print("[ERROR]\tbad center occured skip.")
                continue
            if tempScore < score:
                resList = self.coreList
                score = tempScore
                conn = 0
            else:
                conn += 1
        # 还原最佳聚类现场以便后续画图
        self.coreList = resList
        self.calc()
        print('[info]\tdes finish with best score %f' % score)
        print(resList)
        return resList


def dis(obj1: list, obj2: list):
    assert isinstance(obj1, list), \
        '[ERROR] 第一个参数应当为list,输入的参数类型为$s' % str(type(obj1))
    assert isinstance(obj2, list), \
        '[ERROR] 第二个参数应当为list,输入的参数类型为$s' % str(type(obj2))
    return sqrt((obj1[1] - obj2[1]) ** 2 + (obj1[2] - obj2[2]) ** 2)


if __name__ == '__main__':
    exp = Classifier()
    for i in range(3, 20):
        print('[center counter]\t%d' % i)
        exp.des(i)
        exp.draw()
