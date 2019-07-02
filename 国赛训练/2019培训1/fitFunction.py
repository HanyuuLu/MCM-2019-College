# 给出的是直径
def diaFun(x: float)->float:
    if x >= 0 and x <= 1.435:
        return 0.0007087*x**3 - 0.01688*x**2 + 0.03858*x + 0.007126
    elif x > 1.435 and x <= 1.585:
        return -1.48253205e-14*x**3 + 6.84091811e-14*x**2 - -1.05053092e-13*x + 3.64500000e-02
    elif x > 1.585 and x <= 2.362:
        return -0.002256*x**3 + 0.004508*x**2 + 0.0001647*x + 0.02781
    elif x > 2.362 and x <= 2.640:
        return -0.2623*x**2 + 1.279*x - 1.546
    else:
        return 0

# 半径


def fitFun(x: float)->float:
    return (diaFun(x))/2

# 标枪参数自身描述常量类


class LimitRange:
    def __init__(self):
        # 长轴上下限
        self.UPPER_LIMIT = 2.640
        self.LOWER_LIMIT = 0
        # 计算精度
        self.DISP = 1e-3
        # 出手位置
        self.INITIAL_X = 0
        self.INITIAL_Y = 2.000
        # 重量
        self.WEIGHT = 0.8
        # 质心位置
        self.POS_FOCUS = 1.345734932207
        # 脱手持枪角
        self.INITIAL_THETA = 36.6-0.9
        # 初始攻角
        self.INITIAL_BETA = -0.9
        # 初始角速度
        self.INITIAL_VTHETA = 0
        # 标枪密度
        self.B_RHO = 592.961619248255
        # 转动惯量
        self.B_J = 25.181045013632765
        # 质心到杆前端的距离
        self.TOUCH_LENGTH = 1.294265067793
        # 体积
        self.volume = 0.0013491598343485102
        # 初速度
        self.INITIAL_SPEED = 30
# 空气参数


class Air:
    def __init__(self, *args, **kwargs):
        self.RHO = 1.184
        self.CP = 1.2
        self.CF = 0.003
        # self.CF = 0.0032298852845135534
        # self.CP = -0.13666819606128208
        self.CP = 0.058193268
        self.CF = 0.003180604
        self.GRAVITY = 9.8  # N/g
