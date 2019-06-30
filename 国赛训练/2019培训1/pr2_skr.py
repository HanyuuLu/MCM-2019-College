import xlrd
from sklearn import linear_model
import sys



if __name__ == "__main__":
	try:
		fileName = sys.argv[-1]
	except Exception:
		print('[error] Please input file name')
		exit()
	x = list()
	y = list()
	try:
		workbook = xlrd.open_workbook(fileName)
		sheet = workbook.sheet_by_index(0)
		for i in range(sheet.nrows):
			tempX = list()
			for j in range(sheet.ncols-1):
				tempX.append(sheet.cell(i,j).value)
			x.append(tempX)
			y.append(sheet.cell(i,sheet.ncols-1).value)
	except Exception:
		print('[error] There is problem with input file name %s'%fileName)
		exit()
	print('[info] file %s loaded successfully, fitting for the model'%fileName)
	clf = linear_model.LinearRegression()
	# print(x)
	# print(y)
	clf.fit(x,y)

	regress_coefs = clf.coef_
	regress_intercept = clf.intercept_
	print('[param]\t',clf.get_params())
	for i in range(len(regress_coefs)):
		print('[INT %d]\t%f'%(i,regress_coefs[i]))
	print('[coef]\t%f'%regress_intercept) 
	print('[score]\t',clf.score(x,y))

