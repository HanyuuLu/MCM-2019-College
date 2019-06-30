class Obj:
	def __init__(self,length,posFocus,weight, *args, **kwargs):
		super().__init__(*args, **kwargs)
		self.LENGTH = length
		self.POS_FOCUS = posFocus
		self.WEIGHT= weight