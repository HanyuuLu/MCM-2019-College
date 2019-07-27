import sys
import gc
sys.path.append('.\\')
from core.classifier import Classifier
from core.configIO import fetchConfigList
if __name__ == '__main__':
    configList = fetchConfigList()
    obj = Classifier()
    for conf in configList:
        print(conf)
        gc.collect()
        obj.loadConfig(conf)
        obj.calc()
        obj.score()
        obj.draw()