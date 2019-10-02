import scipy.stats as stats
import json


def calc(n=5):
    n = n
    carSpeed = 2
    humanSpeed = 1.4
    carLength = 4
    carMargin = 1.5
    waitingLength = 3
    roadWidth = 3
    conTime = 1
    safeLock = [False, False]
    time = [0, 0]
    timeOnStop = [[0] * n, [0] * n]
    prepareTime = [[0] * n, [0] * n]
    prepared = [[False] * n, [False] * n]
    state = [0, 0]
    counter = 0
    # 0 无状态 1 车辆进入 2 停止 3 车辆驶出
    t = (n * (carLength + carMargin) - carMargin + waitingLength) / carSpeed
    incomeTime = [t, t + 1]
    outTime = (n * (carLength + carMargin) - carMargin) / carSpeed
    keyTime = 0
    position = list()
    for i in range(n):
        for j in range(2):
            position.append([2+5.5*i, j % 2*3])
    locaiton = [(position[0][0]+position[-1][0])/2, 0]
    locaiton = [position[-1][0]+2, 0]
    while keyTime < 60*60:
        for i in range(2):
            # 更新人员信息
            if (i == 0 and safeLock[0] and safeLock[1]) or \
                    (i == 1 and safeLock[1]):
                for j in range(n):
                    while True:
                        res = stats.expon(scale=1/0.0305).rvs()
                        if res < 72:
                            break
                    if prepared[i][j] is False:
                        prepareTime[i][j] = int(
                            (abs(position[2 * j + i][0] - locaiton[0]) +
                             abs(position[2 * j + i][1] - locaiton[1]) +
                                res)/humanSpeed+keyTime
                        )
                        prepared[i][j] = True

            # 更新车体信息
            if state[i] == 0:
                time[i] = keyTime
                state[i] = 1
                continue
            elif state[i] == 1:
                if time[i] + incomeTime[i] <= keyTime:
                    state[i] = 2
                    time[i] = keyTime
                    safeLock[i] = True
                continue
            elif state[i] == 2:
                for j in range(n):
                    if not prepared[i][j]:
                        break
                    for j in range(1, n):
                        prepareTime[i][j] = max(
                            prepareTime[i][j - 1] + 2, prepareTime[i][j])
                    if keyTime >= prepareTime[i][-1]:
                        for j in range(n):
                            timeOnStop[i][j] += prepareTime[i][j]-time[i]
                            prepared[i][j] = False
                        # print(prepareTime)
                        state[i] = 3
                        time[i] = keyTime
                        safeLock[i] = False
                        break
                continue
            elif state[i] == 3:
                if time[i] + outTime <= keyTime:
                    time[i] = keyTime
                    state[i] = 1
                    counter += n
                    continue
        keyTime += 1
        # print(keyTime)
    res = dict()
    res['车位数'] = n
    res['一小时过车计数'] = counter
    res['停滞时间'] = timeOnStop
    return res


if __name__ == '__main__':
    res = dict()
    for i in range(5,6):
        res[i] = calc(i)
    with open('./res.json', 'w') as w:
        json.dump(res, w)