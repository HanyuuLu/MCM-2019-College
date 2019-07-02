from flyCalcSysP4 import Obj
from dataReader import multiXreaderSPC
import math


class GradidentDesend:
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.deltaBeta = 1
        self.deltaTheta = 1
        self.deltaOmega = 1
        self.learningRate = 1
        self.obj = Obj()
        self.beta = self.obj.INITIAL_BETA
        self.theta = self.obj.INITIAL_THETA
        self.omega = self.obj.INITIAL_OMEGA
        self.Y = list()
        self.record = list()
        # print(self.data)

    def execSig(self):
        self.obj.reset()
        res = self.obj.calc()
        return(res)

    def exec(self):
        count = 0
        while count < 1000:
            self.series = [
                [self.beta+self.deltaTheta, self.theta, self.omega],
                [self.beta-self.deltaTheta, self.theta, self.omega],
                [self.beta, self.theta+self.deltaBeta, self.omega],
                [self.beta, self.theta-self.deltaBeta, self.omega],
                [self.beta, self.theta, self.omega+self.deltaOmega],
                [self.beta, self.theta, self.omega-self.deltaOmega],
            ]
            self.seriesRes = list()
            print('\r[batch %d]' % (count), end='  ')
            for x in self.series:
                self.obj.INITIAL_BETA = x[0]
                self.obj.INITIAL_THETA = x[1]
                self.obj.INITIAL_OMEGA = x[2]
                self.Y.append(self.execSig())
            self.beta += (self.Y[0] - self.Y[1])*self.learningRate
            self.theta += (self.Y[2] - self.Y[3])*self.learningRate
            self.omega += (self.Y[4] - self.Y[5])*self.learningRate
            self.record.append([self.beta, self.theta, self.omega, sum(self.Y)/6])
            self.Y.clear()
            print(self.record[-1])
            count += 1
            if (len(self.record) > 10):
                if (self.deltaBeta < 1e-4 and self.deltaTheta < 1e-4 and self.deltaOmega<1e-4):
                    print('[finished]')
                    print('[wind speed]%f'%self.obj.WIND_SPEED)
                    exit()
                if (self.record[-1][2] * 10 < sum([x[2] for x in self.record[-10:]])):
                        self.deltaBeta /= 2
                        self.deltaTheta /= 2
                        self.deltaOmega /= 2
                        print('[Delta became smaller][deltaBeta:%f,deltaTheta:%f,deltaOmega:%f]' % (
                            self.deltaBeta, self.deltaTheta,self.deltaOmega))


if __name__ == '__main__':
    grd = GradidentDesend()
    grd.exec()
