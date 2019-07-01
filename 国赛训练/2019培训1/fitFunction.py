# 给出的是直径
def diaFun(x:float)->float:
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

# 半径
def fitFun(x:float)->float:
	return (diaFun(x))/2

# 标枪参数自身描述常量类
class LimitRange:
	def __init__(self):
		# 长轴上下限
		self.UPPER_LIMIT = 2640
		self.LOWER_LIMIT = 0
		# 计算精度
		self.DISP = 1e-3
		# 出手位置
		self.INITIAL_X = 0
		self.INITIAL_Y = 2
		# 重量
		self.WEIGHT=600
		# 质心位置
		self.POS_FOCUS = 1345.734932207
		# 脱手持枪角
		self.INITIAL_THETA = 36.6
		# 初始攻角
		self.INTITIAL_BETA = -0.9
		# 初始角速度
		self.INITIAL_VTHETA = 0
		# 标枪密度
		self.B_RHO = 600/19268155911.623592
		# 转动惯量
		self.B_J = 41239562955.83207
# 空气参数
class Air:
	def __init__(self, *args, **kwargs):
		self.RHO = 1.184e-6
		self.CP = 0
		self.CF = 0
		self.GRAVITY = 9.8 # N/g