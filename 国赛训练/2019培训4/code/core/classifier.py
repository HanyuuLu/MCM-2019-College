import os
from json import dumps
from math import sqrt
from random import randint, random

import matplotlib.pyplot as plt

# import core.const
from core import const
from core.configIO import configWrite, fetchConfigList
from core.const import OUTPUT_PATH
from core.dataReader import dataReader


class Classifier:
    # 初始化、读入数据库、标定数据范围
    def __init__(self):
        # 原始数据
        self.rawData = dataReader()[0]
        # 下标下限
        self.LOWER_LIMIT = 0
        # 下标上限
        self.UPPER_LIMIT = len(self.rawData) - 1
        # 输出结果路径
        self.OUTPUT = OUTPUT_PATH
        if not os.path.exists(self.OUTPUT):
            os.makedirs(self.OUTPUT)
            print('⚠[INFO]\t output folder doesn\'t exists, created')

    # 导入配置
    def loadConfig(self, configList: list):
        self.typeCount = configList[0]
        self.coreList = configList[1]
        assert self.typeCount == len(self.coreList),'[ERROR]\t 错误配置'

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
        # print('😜✔[info] calc finished')

    # 绘制聚类图
    def draw(self):
        plt.rcParams['font.sans-serif'] = ['SimHei']
        plt.rcParams['axes.unicode_minus'] = False
        plt.figure(
            figsize=(
                const.FIGURE_WIDTH,
                const.FIGURE_HEIGHT
            ),
            dpi=const.FIGURE_DPI
        )
        plt.xlim(const.LONGITUDE_LOWER, const.LONGITUDE_UPPER)
        plt.ylim(const.LATITUDE_LOWER, const.LATITUDE_UPPER)
        plt.xlabel('经度/°E')
        plt.ylabel('纬度/°N')
        plt.title(
            '%d centers with average distance %.4f'
            % (self.typeCount, self.totalAverage)
        )
        # print(str(self.coreList))
        handerList = list()
        for i in self.classList:
            col = (random(), random(), random())
            handerList.append(
                plt.plot([x[2] for x in i], [x[1] for x in i],
                         'x', color=col)
            )
        # plt.text(112.74, 23.8, str(self.coreList), ha='left', fontsize=8)
        plt.legend(self.coreList)
        plt.draw()
        # plt.show()
        # plt.text(4, 1, t, ha='left', rotation=15, wrap=True)
        fileName = os.path.join(self.OUTPUT, '%s.jpg' % str(self.typeCount))
        plt.savefig(fileName)

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
        # 每个聚类的最优化数据（聚类个数，中心点数据被持久化保存）
        configWrite(self.typeCount, self.coreList)
        # 计算最优化数据的分数
        self.calc()
        print('[info]\tdes finish with best score %f' % score)
        print(resList)
        return resList

    # 分析附录一每个群组的情况
    def processGroup(self):
        configList = fetchConfigList()
        for conf in configList:
            self.typeCount = conf[0]
            self.coreList = conf[1]
            self.calc()
            # 统计数据
            res = list()
            for group in self.classList:
                res.append(dict())
                if len([x[3] for x in group]):
                    res[-1]['avg'] = round(
                        sum([x[3] for x in group])/len([x[3] for x in group]),
                        4
                    )
                else:
                    res[-1]['avg'] = None
                p = [x[3] for x in group if x[4] == 1]
                a = [x[3] for x in group if x[4] == 0]
                label = ('完成', '未完成')
                data = (p, a)
                for i in range(len(label)):
                    res[-1][label[i]] = {'len': len(data[i])}
                    if res[-1][label[i]]['len'] != 0:
                        res[-1][label[i]].update(
                            {
                                'max': max(data[i]),
                                'min': min(data[i]),
                                'avg': round(sum(data[i]) / len(data[i]), 4)
                            }
                        )
                if len(p) + len(a) == 0:
                    res[-1]['成交/总'] = None
                else:
                    res[-1]['成交/总'] = round(len(p)/(len(p)+len(a)), 4)
            fileNameWithPath = os.path.join(
                self.OUTPUT, str(self.typeCount) + '.json')
            try:
                with open(fileNameWithPath, 'w') as w:
                    w.write(dumps({
                        '聚类数': self.typeCount,
                        '聚类核心号': self.coreList,
                        '聚类统计数据': res
                    }))
            except Exception as e:
                print('[ERROR]\t %s😂💔' % str(e))


def dis(obj1: list, obj2: list):
    assert isinstance(obj1, list) or isinstance(obj1,tuple), \
        '[ERROR] 第一个参数应当为list或者tuple,输入的参数类型为%s' % str(type(obj1))
    assert isinstance(obj2, list) or isinstance(obj2,tuple), \
        '[ERROR] 第二个参数应当为list或者tuple,输入的参数类型为%s' % str(type(obj2))
    return sqrt((obj1[1] - obj2[1]) ** 2 + (obj1[2] - obj2[2]) ** 2)
