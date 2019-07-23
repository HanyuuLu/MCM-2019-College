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


def fit(data: list, core: list):
    if len(data) == 0:
        return None
    tmpList = dict()
    for i in data:
        if i[3] in tmpList:
            tmpList[i[3]][i[4]] += 1
        else:
            tmpList[i[3]] = [0, 0]
            tmpList[i[3]][i[4]] += 1
    # for i in tmpList:
    #     tmpList[i] = tmpList[i][1] / sum(tmpList[i])
    # px
    px = dict()
    for i in tmpList:
        px[i] = sum(tmpList[i])/sum([sum(tmpList[key]) for key in tmpList])
    # qx
    qx = dict()
    for i in tmpList:
        qx[i] = tmpList[i][1] / sum(tmpList[i])
    # score
    score = dict()
    for i in px:
        score[i] = 0.7 * px[i] + 0.3 * qx[i]
        score[i] = round(score[i], 6)
    m = max([score[x] for x in score])
    res = [key for key in score if score[key] == m]
    pos = (core[2], core[1])
    rtnRes = list()
    for i in range(len(res)):
        rtnRes.append({'no': res[i], 'E': pos[0], 'N': pos[1]})
    return rtnRes


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
        y = pol[0]*x+pol[1]
        axs[i].plot(x, y)
    fileName = os.path.join(OUTPUT_PATH, 'P01point%d.jpg' % calc.typeCount)
    plt.savefig(fileName)


if __name__ == "__main__":
    configList = fetchConfigList()
    calc = Classifier()
    for conf in configList:
        calc.loadConfig(conf)
        calc.calc()
        resList = list()
        for group in calc.classList:
            core = calc.rawData[calc.coreList[calc.classList.index(group)]]
            resList.append(fit(group, core))
        fileName = os.path.join(
            OUTPUT_PATH, 'P01point%d.json' % calc.typeCount)
        with open(fileName, 'w') as w:
            w.write(dumps(resList))
        print(fileName)
        # draw(resList)
