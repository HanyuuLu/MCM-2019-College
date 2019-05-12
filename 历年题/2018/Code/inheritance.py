from random import randint
from RGV import RGV
import gc
import numpy
SEED_LENGTH = 10000  # 序列长度
MACHINE_COUNT = 8  # 机器总数
UUID = 0
ORIGIN_SIZE = 20  # 父群个数
CHILD_SIZE = 4  # 子群个数

# 种群


class Group:
    # 初始化一个种群
    def __init__(self):
        self.originList = []
        self.childList = []
    def init(self):
        count = 0
        while True:
            count+=1
            for _ in range(ORIGIN_SIZE):
                self.originList.append(Item())
            for _ in range(int(ORIGIN_SIZE*CHILD_SIZE/2)):
                self.cross()
            for i in self.childList:
                rgv = RGV(0,1)
                i.output = rgv.goAlong(i.alignment)
            self.childList.sort(key=lambda i:i.output[0],reverse = True)
            for i in self.childList:
                print(i.output[0], end=' ')
            print("\n[count] %d" % count)
            print("[best] %d"% self.childList[0].output[0])
            del (self.originList)
            self.originList = self.childList[:ORIGIN_SIZE]
            for i in self.originList:
                i.alignment=self.variation(i.alignment)
            del (self.childList)
            self.childList = []
    # 交叉操作
    def cross(self):
        slice = randint(0, SEED_LENGTH)
        parentsA = randint(0, ORIGIN_SIZE-1)
        parentsB = randint(0, ORIGIN_SIZE-1)
        resA = self.originList[parentsA].alignment[:slice]
        resB = self.originList[parentsB].alignment[:slice]
        resA.extend(self.originList[parentsA].alignment[slice:])
        resB.extend(self.originList[parentsA].alignment[slice:])
        # self.childList.append(Item(self.variation(resA)))
        # self.childList.append(Item(self.variation(resB)))
        self.childList.append(Item(resA))
        self.childList.append(Item(resB))
    def variation(self, inputList):
        if randint(0, 10) >8:
            assert len(inputList)==SEED_LENGTH
            a = randint(0, SEED_LENGTH)
            b = randint(0, SEED_LENGTH)
            c = min(a, b)
            d = max(a, b)
            del (a)
            del (b)
            if c == d:
                return inputList
            res = inputList[:c]
            rev = inputList[c:d]
            rev.reverse()
            res.extend(rev)
            res.extend(inputList[d:])
            assert len(res)==SEED_LENGTH
            return res
        return inputList



# 个体


class Item:
    # 随机/根据给定序列产生一个个体
    def __init__(self, *inputList):
        global SEED_LENGTH
        global MACHINE_COUNT
        global UUID
        self.uuid = UUID
        self.output = None
        UUID += 1
        self.alignment = []
        # 指定赋值
        if len(inputList) == 1:
            assert isinstance(inputList[0], list), \
                "[Hanyuu]应当使用列表对象初始化个体,输入对象类型为" + str(type(inputList[0]))
            self.alignment = inputList[0]
            assert max(self.alignment) < MACHINE_COUNT and min(self.alignment) >= 0, \
                "[Hanyuu]输入数组的最大值/最小值超限，max = %d, min = %d" % (
                    max(self.alignment), min(self.alignment))
            assert len(self.alignment) == SEED_LENGTH, \
                "[Hanyuu]输入的初始化列表序列长度应当为%d,输入长度为%d" % (
                SEED_LENGTH, len(self.alignment))
            return
        # 随机产值
        for i in range(SEED_LENGTH):
            self.alignment.append(randint(0, MACHINE_COUNT - 1))
    # 析构函数

    def __del__(self):
        del(self.uuid)
        del (self.alignment)
        gc.collect()

def test():
    group = Group()
    group.init()

if __name__ == '__main__':
    test()
