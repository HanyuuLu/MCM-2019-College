import fitFunction
import numpy

class Volume(fitFunction.LimitRange):
	def __init__(self, *args, **kwargs):
		super().__init__()
	def calc(self):
		vol = 0
		for x in numpy.arange(self.LOWER_LIMIT,self.UPPER_LIMIT,self.DISP):
			vol += fitFunction.fitFun(x)**2
			if x%1e-3==0:
				print('\rprocessing %f,%f.2%%'%(x,(x-self.LOWER_LIMIT)/(self.UPPER_LIMIT-self.LOWER_LIMIT)*100),end = '')
		print('')
		from math import pi
		vol = vol*pi*self.DISP
		return vol
if __name__=='__main__':
	a = Volume()
	print(a.calc())
