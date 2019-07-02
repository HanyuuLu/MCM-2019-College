from fitFunction import diaFun	#直径
from fitFunction import LimitRange,Air
import numpy
import math
from math import degrees
from math import radians
from numpy import sign

class Obj(LimitRange,Air):
	def __init__(self,*args, **kwargs):
		LimitRange.__init__(self)
		Air.__init__(self)
		self.S0 = 0.06412420498140184	# 投影面积
		self.M_TMP = 9.618450686734025
		#平动
		self.Xx = self.INITIAL_X
		self.Xy = self.INITIAL_Y
		self.Vx = math.cos(radians(self.INITIAL_THETA))*self.INITIAL_SPEED
		self.Vy = math.sin(radians(self.INITIAL_THETA))*self.INITIAL_SPEED
		self.Ax = 0
		self.Ay = 0
		# 转动
		self.theta = self.INITIAL_THETA
		self.Vtheta = self.INITIAL_VTHETA
		self.Atheta = 0
		self.beta = self.INITIAL_BETA
	# Reset status
	def reset(self):
		self.Xx = self.INITIAL_X
		self.Xy = self.INITIAL_Y
		self.Vx = math.cos(radians(self.INITIAL_THETA))*self.INITIAL_SPEED
		self.Vy = math.sin(radians(self.INITIAL_THETA))*self.INITIAL_SPEED
		self.Ax = 0
		self.Ay = 0
		# 转动
		self.theta = self.INITIAL_THETA
		self.Vtheta = self.INITIAL_VTHETA
		self.Atheta = 0
		self.beta = self.INITIAL_BETA
	# 标枪投影面积
	def S0Calc(self):
		print('calculating')
		S = 0
		for x in numpy.arange(self.LOWER_LIMIT,self.UPPER_LIMIT,self.DISP):
			S+=diaFun(x)
		S*=self.DISP
		self.S0 = S
		print('calculating finished')
		return S
	def M_TMPCalc(self):
		print('calculating')
		S = 0
		for x in numpy.arange(self.LOWER_LIMIT,self.UPPER_LIMIT,self.DISP):
			S+=diaFun(x)*(x-self.POS_FOCUS)**2
		S*=self.DISP/2*self.B_RHO*self.CP
		self.M_TMP = S
		print('calculating finished')
		return S
	def FpyCalc(self):
		res = (self.Vx*math.cos(radians(self.beta)))**2*math.sin(radians(self.theta))
		res *= -sign(self.beta) * self.RHO * self.CP* self.S0
		return res
	def FpzCalc(self):
		res = (self.Vy*math.cos(radians(self.beta)))**2*math.cos(radians(self.theta))
		res *= -sign(self.beta) * self.RHO * self.CP* self.S0
		return res
	def FfyCalc(self):
		res = (self.Vx*math.sin(radians(self.beta)))**2*math.cos(radians(self.theta))
		res *= -math.pi/2 * self.RHO * self.CF*self.S0
		return res
	def FfzCalc(self):
		res = (self.Vy*math.sin(radians(self.beta)))**2*math.sin(radians(self.theta))
		res *= -math.pi/2 * self.RHO * self.CF*self.S0
		return res
	def Fx(self):	# Y轴
		return self.FpyCalc()+self.FfyCalc()
	def Fy(self):	# Z轴
		return self.FpzCalc()+self.FfzCalc()-self.WEIGHT*self.GRAVITY
	def M(self):	# 转动力矩
		return self.M_TMP*sign(self.beta)*(self.Vx**2+self.Vy**2)*(math.cos(self.beta)**2)
	def linearUpdate(self):
		self.Xx+=self.DISP*self.Vx
		self.Xy+=self.DISP*self.Vy
		self.Ax=self.Fx()/self.WEIGHT
		self.Ay=self.Fy()/self.WEIGHT
		self.Vx+=self.DISP*self.Ax
		self.Vy+=self.DISP*self.Ay
	def rotationUpdate(self):
		self.theta+=self.Vtheta*self.DISP
		self.Atheta = degrees(self.M()/self.B_J)
		self.Vtheta+=self.DISP*self.Atheta
		self.beta = self.theta-degrees(math.atan(self.Vy/self.Vx))
	def calc(self):
		key = 0
		# print(self.Xy+math.sin(radians(self.theta))*self.TOUCH_LENGTH)
		while (self.Xy+math.sin(radians(self.theta))*self.TOUCH_LENGTH)>0:
			key+=1
			self.linearUpdate()
			self.rotationUpdate()
		# 	if key%1000==0:
		# 		print('%.1f sec\t%f\t%f\t\t%f\t%f'%(key*self.DISP,self.Xx,self.Xy,self.Vx,self.Vy))
		# print('')
		# print('[x]%f'%self.Xx)
		return self.Xx

if __name__=='__main__':
	obj = Obj()
	# print(obj.S0Calc())
	# print(obj.M_TMPCalc())
	print(obj.calc())


