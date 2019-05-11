class CNC:
    def __init__(self, id, no=0):
        assert id>=-1 and id<8
        self.label = id  					# 刀具标识
        self.id = id                        # 机器编号
        self.position = (int)(id/2)         # 机器位置编号
        self.isProduct = False		    	# 是否具有产品
        self.signal = False			    	# 信号
