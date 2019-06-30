class Obj:
	def __init__(self,length,posFocus,weight, *args, **kwargs):
		self.LENGTH = length
		self.POS_FOCUS = posFocus
		self.WEIGHT= weight
		return super().__init__(*args, **kwargs)