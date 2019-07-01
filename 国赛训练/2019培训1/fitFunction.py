# 给出的是半径
def fitFun(x:float)->float:
	if x>=0 and x<=1435:
		return 7.087e-10*x**3 - 1.688e-05*x**2 + 0.03858*x + 7.126
	elif x>1435 and x<=1585:
		return -5.234e-21*x**3 + 2.266e-17*x**2 - 3.261e-14*x + 36.45
	elif x>1585 and x<=2362:
		return -2.256e-09*x**3 + 4.508e-06*x**2 + 0.0001647*x + 27.81
	elif x>2362 and x<=2640:
		return -2.209e-06*x**3 + 0.01631*x**2 - 40.15*x + 3.295e+04
	else:
		return 0

# 标枪参数自身描述常量类
class LimitRange:
	def __init__(self):
		self.UPPER_LIMIT = 2640
		self.LOWER_LIMIT = 0
		self.DISP = 1e-3