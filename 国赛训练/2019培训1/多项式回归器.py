import numpy as np
import matplotlib.pyplot as plt
from polyDraw import draw as draw
from dataReader import reader as reader

def polynomialFit(x:list,y:list):
	#定义x、y散点坐标
	# x = [10,20,30,40,50,60,70,80]
	x = np.array(x)
	# print('x is :\n',x)
	# num = [174,236,305,334,349,351,342,323]
	y = np.array(y)
	# print('y is :\n',y)
	#用3次多项式拟合
	f1 = np.polyfit(x, y, 2)
	print('f1 is :\n',f1)

	p1 = np.poly1d(f1)
	print('p1 is :\n',p1)

	#也可使用yvals=np.polyval(f1, x)
	yvals = p1(x)  #拟合y值
	# print('yvals is :\n',yvals)
if __name__=='__main__':
	data = reader()
	key = 0
	for i in data:
		print('=== sheet %d ===' % key)
		key+=1
		polynomialFit(i[0],i[1])