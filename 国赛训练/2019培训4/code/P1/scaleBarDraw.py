import matplotlib.pyplot as plt
import os
import re
import json
import sys
sys.path.append('.\\')
from core.const import OUTPUT_PATH

if __name__ == '__main__':
    plt.rcParams['font.sans-serif'] = ['SimHei']
    plt.rcParams['axes.unicode_minus'] = False
    for (folder, subFolder, fileName) in os.walk(OUTPUT_PATH):
        for i in fileName:
            if re.match(r'^.*\.json', i):
                with open(os.path.join(folder, i)) as w:
                    rawData = w.read()
                data = json.loads(rawData)
                data = data['聚类统计数据']
                res = list()
                for i in data:
                    res.append(i['成交/总'])
                print(res)
                for x in range(len(res)):
                    if res[x] is None:
                        res[x] = 0
                plt.clf()
                plt.title('%d centers 成交/总' % len(res))
                plt.ylim(0, 1)
                plt.bar(list(range(len(res))), res)
                # plt.show()
                fileName = os.path.join(
                    folder, 'scale%s.jpg' % str(len(res)))
                plt.savefig(fileName)
