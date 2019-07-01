# 转动惯量
class Object:
	def __init__(self,weight,centerPos,rou,disp=1e-5):
		self.WEIGHT = weight
		self.CENTER_POS = centerPos
		self.DISP = disp
		self.ROU=rou
	def calc(self,upLimit,downLimit=0):
		from fitFunction import fitFun
		from math import pi
		import numpy
		J=0
		for x in numpy.arange(downLimit,upLimit,self.DISP):
			J+=abs(fitFun(x)*abs(x-self.CENTER_POS)**2)
			if x % 1e-2 ==0:
				per = (x-downLimit)/(upLimit-downLimit)*100
				print('\rcalcuing position %f, %f%% '%(x,per),end = ' ')
		print('')
		J=J*self.DISP*self.ROU*pi
		return J
if __name__=='__main__':
	a=Object(600,1445.734932,1,1e-3)
	print(a.calc(2640,0))
		

