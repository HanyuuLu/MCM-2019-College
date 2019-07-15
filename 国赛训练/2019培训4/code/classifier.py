from math import sqrt
from dataReader import dataReader
from random import randint


class Classifier:
    def __init__(self):
        self.rawData = dataReader()[0]

    def calc(self, typeCount: int):
        self.LOWER_LIMIT = 0
        self.UPPER_LIMIT = len(self.rawData) - 1
        self.coreList = list()
        while len(self.coreList) < typeCount:
            key = randint(self.LOWER_LIMIT, self.UPPER_LIMIT)
            if key in self.coreList:
                continue
            self.coreList.append(key)
        self.classList = [list() for _ in range(typeCount)]
        for i in self.rawData:
            key = float('inf')
            ptr = -1
            for j in self.coreList:
                distance = dis(i, self.rawData[j])
                if key > distance:
                    ptr = self.coreList.index(j)
                    key = distance
            self.classList[ptr].append(i)
        print('calc finished 😂')


def dis(obj1: list, obj2: list):
    return sqrt((obj1[1] - obj2[1]) ** 2 + (obj1[2] - obj2[2]) ** 2)


if __name__ == '__main__':
    exp = Classifier()
    exp.calc(20)
