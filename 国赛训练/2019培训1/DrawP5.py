from flyCalcSysP5 import Obj
from polyDraw import draw
class Draw:
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.obj = Obj()
        self.speed = self.obj.INITIAL_SPEED
        self.theta = self.obj.INITIAL_THETA
        self.beta = self.obj.INITIAL_BETA
        self.omega = self.obj.INITIAL_OMEGA

    def execSig(self):
        self.obj.reset()
        res = self.obj.calc()
        return (res)
        # 出手速度
        # 出手角
        # 初始攻角
        # 初始俯仰角速度
        # 风向及风速
    def exec(self):
        self.series = [
            self.omega - 8,
            self.omega - 4,
            self.omega,
            self.omega + 2,
            self.omega + 4
        ]
        resList = list()
        for x in self.series:
            self.obj.INITIAL_OMEGA = x
            res = self.execSig()
            print(res[0])
            resList.append(res[-2:])
        draw(resList)
if __name__ == '__main__':
    d = Draw()
    d.exec()