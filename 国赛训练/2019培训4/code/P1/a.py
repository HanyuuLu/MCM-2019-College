import matplotlib.pyplot as plt
import numpy as np
from core.const import OUTPUT_PATH
from core.configIO import fetchConfigList
from core.classifier import Classifier
import sys
from json import dumps
import os
sys.path.append('.\\')
print(OUTPUT_PATH)


def fit(data: list):
    if len(data) == 0:
        return None
    tmpList = dict()
    for i in data:
        if i in tmpList:
            tmpList[i] += 1
        else:
            tmpList[i] = 1
    x, y = [x for x in tmpList], [tmpList[x] for x in tmpList]
    res = np.polyfit(x, y, 2)
    for i in range(len(res)):
        res[i] = round(res[i], 6)
    return {'poly': list(res), 'min': min(data), 'max': max(data)}
    # return (res, min(data), max(data))


def draw(data: list):
    plt.rcParams['font.sans-serif'] = ['SimHei']
    plt.rcParams['axes.unicode_minus'] = False
    plt.title('poly fit for %d centers' % len(data))
    fig, axs = plt.subplots(len(data), 1, sharex=True)
    fig.subplots_adjust(hspace=0)
    for i in range(len(data)):
        if data[i] is None:
            continue
        min, max = data[i]['min'], data[i]['max']
        pol = data[i]['poly']
        x = np.arange(min, max, 0.1)
        y = pol[0]*x**2+pol[1]*x+pol[2]
        axs[i].plot(x, y)
    fileName = os.path.join(OUTPUT_PATH, 'P01poly%d.jpg' % calc.typeCount)
    plt.savefig(fileName)


if __name__ == "__main__":
    configList = fetchConfigList()
    calc = Classifier()
    for conf in configList:
        calc.loadConfig(conf)
        calc.calc()
        resList = list()
        for group in calc.classList:
            resList.append(fit([x[3] for x in group]))
        fileName = os.path.join(OUTPUT_PATH, 'P01poly%d.json' % calc.typeCount)
        with open(fileName, 'w') as w:
            w.write(dumps(resList))
        print(fileName)
        draw(resList)
