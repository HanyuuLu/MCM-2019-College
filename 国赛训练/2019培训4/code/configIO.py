import glob
import os

configPath = 'config'


def configWrite(typeCounter: int, coreList: list)->None:
    if not os.path.exists(configPath):
        os.makedirs(configPath)
    try:
        with open(os.path.join(configPath, str(typeCounter)+'.config'), 'w') as w:
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
    for fileName in glob.glob(configPath+'\*.config'):
        print(fileName)


if __name__ == '__main__':
    print(configRead(os.path.join(configPath, '3.config')))
