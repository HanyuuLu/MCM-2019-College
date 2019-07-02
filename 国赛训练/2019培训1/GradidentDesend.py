from flyCalcSys import Obj
from dataReader import multiXreaderSPC
import math


class GradidentDesend:
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.deltaCp = 5e-2
        self.deltaCf = 1e-4
        self.obj = Obj()
        self.cf = self.obj.CF
        self.cp = self.obj.CP
        self.deltaY = list()
        self.tempDeltaY = list()
        self.data = multiXreaderSPC()[0]
        self.record = list()
        # print(self.data)

    def execSig(self, x, y):
        self.obj.reset()
        self.obj.INITIAL_SPEED = x[0]
        self.obj.INITIAL_BETA = x[2]
        self.obj.INITIAL_THETA = x[1]-self.obj.INITIAL_BETA
        res = self.obj.calc()
        return((res-y)**2)

    def exec(self):
        count = 0
        while count < 100:
            self.series = [
                [self.cf+self.deltaCf, self.cp],
                [self.cf-self.deltaCf, self.cp],
                [self.cf, self.cp+self.deltaCp],
                [self.cf, self.cp-self.deltaCp],
            ]
            self.seriesRes = list()
            ccount = 0
            print('\r[batch %d, running %d %d/4*24]' %
                  (count, int(ccount/24), ccount % 24), end='  ')
            for x in self.series:
                self.obj.CF = x[0]
                self.obj.CP = x[1]
                for i in range(len(self.data[0])):
                    self.tempDeltaY.append(
                        self.execSig(self.data[0][i], self.data[1][i])
                    )
                    ccount += 1
                    print('\r[batch %d, running %d %d/4*24]' %
                          (count, int(ccount / 24), ccount % 24), end='  ')
                self.deltaY.append(sum(self.tempDeltaY))
                self.tempDeltaY.clear()
            self.cf -= (self.deltaY[0]-self.deltaY[1])/1000*self.deltaCf
            self.cp -= (self.deltaY[2]-self.deltaY[3])/1000*self.deltaCp
            self.record.append([self.cf, self.cp,math.sqrt(sum(self.deltaY)/4/24)])
            self.deltaY.clear()
            print(self.record[-1])
            count += 1
            if (len(self.record) > 5):
                if (self.record[-1][2] * 5 > sum([x[2] for x in self.record[-5:]])):
                        self.deltaCf /= 2
                        self.deltaCp /= 2
                        print('[Delta became smaller][deltaCf:%f,deltaCp:%f]'%(self.deltaCf,self.deltaCp))


if __name__ == '__main__':
    grd = GradidentDesend()
    grd.exec()
