import math

# 系统
class SysInfo:
    def __init__(self, **kwargs):
        super().__init__()
        # 水的密度
        self.thoWater = 1.025e3
        # 水深
        self.WaterDeepth = 18
        # 重力系数
        self.gravityRate = 9.8
        # 风速
        self.WindSpeed  = 12
        

# 节点基类
class Node(SysInfo):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        # 质量
        self.M = kwargs['node']['M']
        # 半径
        self.R = kwargs['node']['R']
        # 高度
        self.H = kwargs['node']['H']
        # 系统倾角
        self.gamma = 0
        # 系统浮力
        self.buoyancy = math.pi * self.R ** 2 * self.H
        # 系统重力
        self.gravity = self.gravityRate*self.M
        # 上位结点的力
        self.alpha = 0
        # 下位结点的力
        self.beta = 0

# 链结
class Chain(Node):
    def __init__(self,**kwargs):
        super().__init__(**kwargs)


# 浮标
class Buoy(Node):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.HeightWaterLine = 0
        self.buoyancy = math.pi * self.R ** 2 *self.HeightWaterLine


# 钢桶
class Drums(Node):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.MBall = kwargs['node']['MBall']


# 钢管
class Pipe(Node):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)


if __name__ == '__main__':
    s = {'M': 20, 'R': 30, 'H': 40, 'gamma': 0}
    node = Node(node=s)
    print(node)
