import glob
import os

configPath = 'output'


def configWrite(typeCounter: int, coreList: list)->None:
    if not os.path.exists(configPath):
        os.makedirs(configPath)
    try:
        fileName = os.path.join(configPath, '%s.config' % str(typeCounter))
        with open(fileName, 'w') as w:
            w.write(str(typeCounter)+'\n')
            for i in coreList:
                w.write(str(i) + '\n')
    except Exception as e:
        print('😔[ERROR]\t%s' % str(e))


def configRead(fileName: str) -> (int, list):
    try:
        with open(fileName, 'r') as r:
            typeCounter = int(r.readline())
            coreList = r.readlines()
            for i in range(len(coreList)):
                coreList[i] = int(coreList[i])
            return (typeCounter, coreList)
    except Exception as e:
        print('😔[ERROR]\t%s' % str(e))


def fetchConfigList() -> tuple:
    fetchConfigList = list()
    for fileName in glob.glob('%s\\*.config' % configPath):
        fetchConfigList.append(configRead(fileName))
    return tuple(fetchConfigList)


if __name__ == '__main__':
    # print(configRead(os.path.join(configPath, '3.config')))
    a = fetchConfigList()
    print(a)
