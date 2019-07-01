import sys
import xlrd

def reader():
	try:
		fileName = sys.argv[-1]
	except Exception:
		print('[error] Please input file name')
		exit()
	resList = list()
	try:
		workbook = xlrd.open_workbook(fileName)
		print('[info] file %s loaded successfully, fitting for the model'%fileName)

		for sheetNo in range(workbook.nsheets):
			sheet = workbook.sheet_by_index(sheetNo)
			x = list()
			y = list()
			for i in range(sheet.nrows):
				x.append(sheet.cell(i,0).value/1000)
				y.append(sheet.cell(i,1).value/1000)
			resList.append([x,y])

	except Exception as e:
		print('[error] There is problem with input file name %s'%fileName)
		exit()
	return resList

def multiXreader():
	try:
		fileName = sys.argv[-1]
	except Exception:
		print('[error] Please input file name')
		exit()
	resList = list()
	x = list()
	y = list()
	try:
		workbook = xlrd.open_workbook(fileName)
		print('[info] file %s loaded successfully, fitting for the model'%fileName)

		for sheetNo in range(workbook.nsheets):
			sheet = workbook.sheet_by_index(sheetNo)
			for i in range(sheet.nrows):
				tempX = list()
				for j in range(sheet.ncols-1):
					tempX.append(sheet.cell(i,j).value/1000)
				x.append(tempX)
				y.append(sheet.cell(i,sheet.ncols-1).value/1000)
			resList.append([x,y])
	except Exception:
		print('[error] There is problem with input file name %s'%fileName)
		exit()
	return resList
