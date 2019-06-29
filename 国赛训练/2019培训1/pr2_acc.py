import pandas


def multiLinerRegressive():
	pass

def getData():
	data=pandas.read_csv('D:\\Repo\\MCM-2019-College\\国赛训练\\2019培训1\\pr_2.data.csv',encoding = 'GBK')
	return data

def drawPlots(data):
	import matplotlib
	from pandas.tools.plotting import scatter_matrix
	font = {'family','SimHei'}
	matplotlib.rc('font',**font)
	scatter_matrix(data=[['speed','angle','attackangle','distance']],figsize=(10,10),diagonal = 'kid')
	data[['speed','angle','attackangle','distance']].corr()
	x=data[['speed','angle','attackangle']]
	y=data[['distance']]
	pass

	pass
if __name__=='__main__':
	drawPlots(getData())
