# 转动惯量
from fitFunction import LimitRange


class Object(LimitRange):
    def __init__(self):
        super().__init__()

    def calc(self):
        from fitFunction import fitFun
        from math import pi
        import numpy
        J = 0
        for x in numpy.arange(self.LOWER_LIMIT, self.UPPER_LIMIT, self.DISP):
            J += abs(fitFun(x)*abs(x-self.POS_FOCUS)**2)
            if x % 1e-2 == 0:
                per = (x-self.LOWER_LIMIT) / \
                    (self.UPPER_LIMIT-self.LOWER_LIMIT)*100
                print('\rcalcuing position %f, %f%% ' % (x, per), end=' ')
        print('')
        J = J*self.DISP*self.B_RHO*pi
        return J


if __name__ == '__main__':
    a = Object()
    print(a.calc())
