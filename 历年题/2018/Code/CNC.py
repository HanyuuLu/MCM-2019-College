class CNC:
	def __init(self,no):
		self.no=no						# 分组号
		self.label = no					# 刀具标识
		# 加工时间表
		# 0:加工完成一道工序所用的物料所需时间
		# 1:加工完成两道工序第一道工序所用的物料所需时间
		# 2:加工完成两道工序第二道工序所用的物料所需时间
		self.processTimeTable = \
			[
				[560,400,378],
				[580,280,500],
				[545,455,182]	
			]
		#上下料时间表
		self.swapTimeTable =  \
			[
				[28,31],
				[30,35],
				[27,32]
			]
		self.isProduct = False			# 是否具有产品
		self.signal=False				# 信号