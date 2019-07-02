from flyCalcSys import Obj
from dataReader import multiXreaderSPC
import math


class GradidentDesend:
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.deltaBeta = 1
        self.deltaTheta = 1
        self.learningRate = 0.1
        self.obj = Obj()
        self.beta = self.obj.INITIAL_BETA
        self.theta = self.obj.INITIAL_THETA
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
                [self.beta+self.deltaTheta, self.theta],
                [self.beta-self.deltaTheta, self.theta],
                [self.beta, self.theta+self.deltaBeta],
                [self.beta, self.theta-self.deltaBeta],
            ]
            self.seriesRes = list()
            print('\r[batch %d]' %(count), end='  ')
            for x in self.series:
                self.obj.INITIAL_BETA = x[0]
                self.obj.INITIAL_THETA = x[1]
                self.Y.append(self.execSig())
            self.beta += (self.Y[0] - self.Y[1])*self.learningRate
            self.theta += (self.Y[2]-self.Y[3])*self.learningRate
            self.record.append([self.beta,self.theta,sum(self.Y)/4])
            self.Y.clear()
            print(self.record[-1])
            count += 1
            if (len(self.record) > 10):
                if (self.deltaBeta <1e-4 and self.deltaTheta < 1e-4):
                    print('[finished]')
                    exit()
                if (self.record[-1][2] * 10 < sum([x[2] for x in self.record[-10:]])):
                        self.deltaBeta /= 2
                        self.deltaTheta /= 2
                        print('[Delta became smaller][deltaBeta:%f,deltaTheta:%f]'%(self.deltaBeta,self.deltaTheta))


if __name__ == '__main__':
    grd = GradidentDesend()
    grd.exec()
