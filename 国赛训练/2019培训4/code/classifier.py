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
        


if __name__ == '__main__':
    exp = Classifier()
    pass
