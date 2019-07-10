class Patient:
    def __init__(self, rawData: list):
        # '序号',  # 0
        # '类型',  # 1
        # '门诊时间',  # 2
        # '入院时间',  # 3
        # '第一次手术时间',  # 4
        # '第二次手术时间',  # 5
        # '出院时间'  # 6
        self.no = rawData[0]
        self.type = rawData[1]
        self.clinicDate = rawData[2]
        self.admissionDate = rawData[3]
        self.operationDate = rawData[4]
        self.secOperaDate = rawData[5]
        self.leaveTime = rawData[6]


if __name__ == '__main__':
    d = [1, 2, 3, 4, 5, 6, 7]
    p = Patient(d)
    print(p)
