import matplotlib.pyplot as plt
import numpy as np
from keras.layers import Dense, normalization, Activation
from keras.models import Sequential
import dataReader
import json
import random


def processData():
    data0 = dataReader.fetchData(0)
    data1 = dataReader.fetchData(1)
    data = dict()
    data['China'] = list()
    data['US'] = list()
    conList = ('China', 'US')
    for key, rawData in enumerate([data0, data1]):
        for label in rawData:
            for record in rawData[label]:
                if 0 in record:
                    continue
                data[conList[key]].append(record[2:])
    with open('data.json', 'w') as w:
        json.dump(data, w)
    print('√[info] data process finished.')


def clac():
    print('▲[info] loading data')
    origData = None
    with open('data.json', 'r') as w:
        origData = json.load(w)

    data = origData['US']
    for record in data:
        for key, item in enumerate(record):
            if item == '':
                record[key] = 0
                continue
            record[key] = float(item)
    # 生成X和y矩阵
    dataMat = np.array(data,dtype=float)
    X = dataMat[:, 1:6]   # 变量x
    y = dataMat[:, 0]  # 变量y
    index = [i for i in range(len(X))]
    random.shuffle(index)
    X = X[index]
    y = y[index]

    res = dict()
    res['times'] = list()
    res['loss'] = list()
    plt.ion()
    # 构建神经网络模型
    model = Sequential()
    model.add(normalization.BatchNormalization(input_shape=(5,)))
    model.add(Activation('sigmoid'))
    model.add(Dense(input_dim=5, units=1))

    # 选定loss函数和优化器
    model.compile(loss='mse', optimizer='sgd')

    cost = 5520000
    cost = 7940000
    # 训练过程
    print('▲[info] training')
    for step in range(100000):
        rawCost = model.train_on_batch(X, y)
        cost = 0.1*rawCost+0.9*cost
        if step % 100 == 0:
            print("After %d trainings, the cost: %f" % (step, cost))
            res['times'].append(step)
            res['loss'].append(cost)
            plt.clf()
            plt.plot(res['times'], res['loss'])
            plt.pause(0.01)

    # 测试过程
    print('\n▲[info] testing')
    cost = model.evaluate(X, y, batch_size=40)
    print('test cost:', cost)
    W, b = model.layers[2].get_weights()
    print('Weights=', W, '\nbiases=', b)
    print('√[info] training finished')
    # # 将训练结果绘出
    # Y_pred = model.predict(X)
    # plt.scatter(X, y)
    # plt.plot(X, Y_pred)
    # plt.show()
    plt.ioff()
    plt.show()


if __name__ == '__main__':
    # processData()
    clac()
