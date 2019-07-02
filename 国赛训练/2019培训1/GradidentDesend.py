from flyCalcSys import Obj
from dataReader import multiXreaderSPC
class GradidentDesend:
	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)
		self.deltaCp = 1e-6
		self.deltaCf = 1e-8
		self.obj = Obj()
		self.cf = self.obj.CF
		self.cp = self.obj.CP
		self.deltaY = list()
		self.tempDeltaY = list()
		self.data = multiXreaderSPC()[0]
		self.record = list()
		# print(self.data)
	def execSig(self,x,y):
		self.obj.reset()
		self.obj.INITIAL_SPEED = x[0]
		self.obj.INITIAL_BETA = x[2]
		self.obj.INITIAL_THETA = x[1]-self.obj.INITIAL_BETA
		res = self.obj.calc()
		return((res-y)**2)
	def exec(self):
		count = 0
		while count<100:
			self.series=[
				[self.cf+self.deltaCf,self.cp],
				[self.cf-self.deltaCf,self.cp],
				[self.cf,self.cp+self.deltaCp],
				[self.cf,self.cp-self.deltaCp],
				]
			self.seriesRes = list()
			for x in self.series:
				self.obj.CF=x[0]
				self.obj.CP=x[1]
				for i in range(len(self.data[0])):
					self.tempDeltaY.append(
						self.execSig(self.data[0][i],self.data[1][i])
					)
				self.deltaY.append(sum(self.tempDeltaY))
				self.tempDeltaY.clear()
			self.cf+=(self.deltaY[0]-self.deltaY[1])/self.deltaCf
			self.cp+=(self.deltaY[2]-self.deltaY[3])/self.deltaCp
			self.record.append([self.cf,self.cp,sum(self.deltaY)/4])
			print(self.cf,self.cp,sum(self.deltaY)/4)
			count+=1






if __name__=='__main__':
	grd = GradidentDesend()
	grd.exec()