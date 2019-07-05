import math


# 节点基类
class Node(SysInfo):
    def __init__(self, **kwargs):
        # 质量
        self.M = kwargs['node']['M']
        # 半径
        self.R = kwargs['node']['R']
        # 高度
        self.H = kwargs['node']['H']
        # 系统倾角
        self.gamma = kwargs['node']['gamma']
        # 系统浮力
        self.buoyancy = math.pi * self.R ** 2 * self.H
        # 系统重力
        self.gravity = self.gravityRate*self.M

# 浮标
class Buoy:
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.HeightWaterLine = kwargs['Bouy']['HeightWaterLine']


# 钢桶
class Drums:
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.MBall = kwargs['Drums']['MBall']


# 钢管
class Pipe:
    def __init__(self, **kwargs):
        super().__init__(**kwargs)


# 系统
class SysInfo:
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.thoWater = 1.025e3
        self.gravityRate = 9.8


if __name__ == '__main__':
    s = {'M': 20, 'R': 30, 'H': 40, 'gamma': 0}
    node = Node(node=s)
    print(node)
