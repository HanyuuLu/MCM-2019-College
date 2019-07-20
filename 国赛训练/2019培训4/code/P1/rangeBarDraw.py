import matplotlib.pyplot as plt
import os
import re
import json
import numpy as np
import sys
sys.path.append('.\\')
from core.const import OUTPUT_PATH

if __name__ == '__main__':
    plt.rcParams['font.sans-serif'] = ['SimHei']
    plt.rcParams['axes.unicode_minus'] = False
    for (folder, subFolder, fileName) in os.walk(OUTPUT_PATH):
        for i in fileName:
            if re.match(r'^.*.json', i):
                with open(os.path.join(folder, i)) as w:
                    rawData = w.read()
                data = json.loads(rawData)
                data = data['聚类统计数据']
                res = list()
                for i in range(4):
                    res.append(list())
                for i in data:
                    if i['完成']['len'] == 0:
                        res[0].append(0)
                        res[1].append(0)
                    else:
                        res[0].append(i['完成']['min'])
                        res[1].append(i['完成']['max'] - i['完成']['min'])
                    if i['未完成']['len'] == 0:
                        res[2].append(0)
                        res[3].append(0)
                    else:
                        res[2].append(i['未完成']['min'])
                        res[3].append(i['未完成']['max']-i['未完成']['min'])
                print(res)
                x = list(range(len(res[0])))
                x = np.arange(len(res[0]))
                width = 0.4
                plt.cla()
                plt.clf()
                plt.ylim(0, 100)
                plt.title('%d centers 成交区间价格' % len(res[0]))
                plt.bar(x-width/2, res[1], bottom=res[0], width=width)
                plt.bar(x+width/2, res[3], bottom=res[2], width=width)
                # plt.show()
                fileName = os.path.join(
                    folder, 'range%s.jpg' % str(len(res[0])))
                plt.savefig(fileName)
