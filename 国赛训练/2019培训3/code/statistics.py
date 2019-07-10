from dataReader import dataReader
import datetime
from draw import draw


class Const:
    def __init__(self):
        self.LABEL = [
            '序号',  # 0
            '类型',  # 1
            '门诊时间',  # 2
            '入院时间',  # 3
            '第一次手术时间',  # 4
            '第二次手术时间',  # 5
            '出院时间'  # 6
        ]
        self.DISEASE = [
            '白内障',  # 0
            '白内障(双眼)',  # 1
            '视网膜疾病',  # 2
            '青光眼',  # 3
            '外伤'  # 4
        ]


class Calc:
    def __init__(self, data):
        self.dateBase = datetime.datetime(2008, 6, 30)
        self.data = data
        self.const = Const()
        # 白内障(单眼)
        self.cataractsS = list()
        # 白内障(双眼)
        self.cataractsD = list()
        # 视网膜疾病
        self.retinalDiseases = list()
        # 青光眼
        self.glaucoma = list()
        # 外伤
        self.trauma = list()
        # 住院人数随时间变化
        self.come = list()
        # 出院时间随人数变化
        self.out = list()
    # 请在总表中计算

    def calcIO(self):
        for _ in range(100):
            self.come.append(0)
            self.out.append(0)
        for sheet in self.data:
            for i in sheet:
                if i[3] != None:
                    self.come[(i[3]-self.dateBase).days] += 1
                if i[6] != None:
                    self.out[(i[6]-self.dateBase).days] += 1
        return [self.come, self.out]

    # TODO
    # 1.各种疾病的平均术后观察时间、等待时间，准备时间。
    # 2.平均每人等待时间（门诊到入院时间）
    # 3.平均每人准备时间（入院到手术）
    # 4.病床周转率（一段时间内的住院人次/（病床数*时间））
    def afterOperation(self):
        self.ao = list()
        for i in range(len(self.const.DISEASE)):
            self.ao.append([0, 0])
        for sheet in self.data:
            for i in sheet:
                if i[1] == self.const.DISEASE[1]:
                    try:
                        self.ao[1][1] += (i[6]-i[5]).days
                        self.ao[1][0] += 1
                    except Exception:
                        pass
                else:
                    key = self.const.DISEASE.index(i[1])
                    try:
                        self.ao[key][1] += (i[6]-i[4]).days
                        self.ao[key][0] += 1
                    except Exception:
                        pass
        res = list()
        for i in self.ao:
            res.append(i[1]/i[0])
        return(res)

    def awaitOperation(self):
        self.ao = list()
        for i in range(len(self.const.DISEASE)):
            self.ao.append([0, 0])
        for sheet in self.data:
            for i in sheet:
                key = self.const.DISEASE.index(i[1])
                try:
                    self.ao[key][1] += (i[3]-i[2]).days
                    self.ao[key][0] += 1
                except Exception:
                    pass
        res = list()
        for i in self.ao:
            res.append(i[1]/i[0])
        return(res)

    def prepOperation(self):
        self.ao = list()
        for i in range(len(self.const.DISEASE)):
            self.ao.append([0, 0])
        for sheet in self.data:
            for i in sheet:
                key = self.const.DISEASE.index(i[1])
                try:
                    self.ao[key][1] += (i[4]-i[3]).days
                    self.ao[key][0] += 1
                except Exception:
                    pass
        res = list()
        for i in self.ao:
            res.append(i[1]/i[0])
        return(res)

    def peopleAwaitOperation(self):
        self.ao = [0, 0]
        for sheet in self.data:
            for i in sheet:
                try:
                    self.ao[1] += (i[3]-i[2]).days
                    self.ao[0] += 1
                except Exception:
                    pass
        res = list()
        res.append(self.ao[1]/self.ao[0])
        return(res)

    def peoplePrepOperation(self):
        self.ao = [0, 0]
        for sheet in self.data:
            for i in sheet:
                try:
                    self.ao[1] += (i[4]-i[3]).days
                    self.ao[0] += 1
                except Exception:
                    pass
        res = list()
        res.append(self.ao[1]/self.ao[0])
        return(res)

    def transRate(self):
        self.ao = [0, 0]
        for sheet in self.data:
            for i in sheet:
                try:
                    self.ao[1] += 1/(i[6]-i[2]).days
                    self.ao[0] += 1
                except Exception:
                    pass
        res = list()
        res.append(self.ao[1]/self.ao[0])
        return(res)


if __name__ == '__main__':
    data = dataReader()
    calc = Calc(data)
    s = calc.transRate()
    const = Const()
    print('病床周转率（平均从到出院的时间的倒数的平均值）')
    # for i in range(5):
    #     print('%s\t%.2f 天'%(const.DISEASE[i],(s[i])))
    print('%.2f人次/天' % s[0])
