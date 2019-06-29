import os
import sys
import csv
import dateConvert
import dataType
import time
DataRoot = './data/csv'
# DataRoot = './expdata/'


def getDataSheet():
    timeFlag = time.time()
    global DataRoot
    fileList = []

    for currentDict, subDict, fileName in os.walk(DataRoot):
        for i in fileName:
            fileList.append(i)
    count = 0
    sum = len(fileList)
    res = {}
    for i in fileList:
        print('[info %2d/%2d, %3.2f%%, %4.2f sec] processing %s' % (count, sum, count/sum*100, time.time()-timeFlag, i ))
        with open(os.path.join(currentDict, i), 'r') as rawInput:
            key = int(i[4:8])
            input = csv.reader(rawInput)
            res[key] = {'mobile': 0, 'card': 0, 'other': 0, 'null': 0}
            filter = {'0.0':'mobile','1.0':'card', 'Null': 'null'}
            for raw in input:
                if raw[3] in filter:
                    res[key][filter[raw[3]]] += 1
                else:
                    if raw[0] == 'ID':
                        continue
                    res[key]['other'] += 1
        count += 1
    print('[info %d/%d, %.2f%%, %.2f sec] task finished' %
              (count, sum, count / sum * 100, time.time() - timeFlag))
    for i in res:
        res[i]['mobile'] += res[i]['null']
        del(res[i]['null'])
    return res


def str2int(num: str) -> int:
    try:
       return int(float(num))
    except Exception as e:
        return None


def draw(res):
    import matplotlib.pyplot as plt
    import pylab
    import matplotlib
    pylab.rcParams['figure.figsize'] = (15.0, 8.0)  # 显示大小
    matplotlib.rcParams['font.sans-serif'] = ['SimHei']
    matplotlib.rcParams['axes.unicode_minus'] = False

    label_list = [x for x in res]
    x = [x for x in range(len(res))]
    num_listMobile = [res[x]['mobile'] for x in res]
    num_listCard = [res[x]['card'] for x in res]
    num_listOther = [res[x]['other'] for x in res]
    rects1 = plt.bar(x=x, height=num_listMobile, width=0.5,
                     alpha=0.8, color='green', label="移动支付")
    rects2 = plt.bar(x=x, height=num_listCard, width=0.5,
                     color='blue', label="刷卡", bottom=num_listMobile)
    btm  = []
    for i in range(len(num_listCard)):
        btm.append(num_listCard[i]+num_listMobile[i])
    rects3 = plt.bar(x=x, height=num_listOther, width=1,alpha = 0.5,color = 'red',label = '其他' , bottom = btm)
    plt.ylabel("人次")
    plt.xticks(x, label_list)
    plt.xlabel("日期/d")
    plt.title("日分布")
    plt.legend()
    plt.show()

if __name__ == '__main__':
    res = getDataSheet()
    draw(res)
