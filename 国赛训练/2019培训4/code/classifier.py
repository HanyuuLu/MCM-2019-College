from  math import sqrt
from dataReader import dataReader
from random import randint


class Classifier:
    def __init__(self):
        self.rawData = dataReader()[0]

    def calc(self, typeCount: int):
        self.LOWER_LIMIT = 0
        self.UPPER_LIMIT = len(self.rawData) - 1
        coreList = list()
        while len(coreList) < typeCount:
            key = randint(self.LOWER_LIMIT, self.UPPER_LIMIT)
            if key in coreList:
                continue
            coreList.append(key)


def dis(obj1: list, obj2: list):
    return sqrt((obj1[1]-obj2[1])**2+(obj1[2]-obj2[2])**2)



if __name__ == '__main__':
    exp = Classifier()
    pass
