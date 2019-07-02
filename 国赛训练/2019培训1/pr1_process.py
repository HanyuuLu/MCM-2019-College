import xlrd
import matplotlib.pyplot as plt
import math
import copy
workbook = xlrd.open_workbook('pr1_data.xlsx')
sheet = workbook.sheet_by_index(0)
data = list()
for i in range(sheet.nrows):
	data.append((sheet.cell(i,0).value/1000,sheet.cell(i,1).value/2000))
count=len(data)-1
orgData = copy.deepcopy(data)
for i in range(count,-1,-1):
	data.append((data[i][0],-data[i][1]))
data.append((data[0][0],data[0][1]))
x=list()
y=list()
for i in data:
	# print(i[0],i[1])
	x.append(i[0])
	y.append(i[1])
plt.plot(x,y,'b-')
# plt.show()
#Area
A=0
for i in range(len(data)-1):
	A+=data[i][0]*data[i+1][1]-data[i+1][0]*data[i][1]
A/=2
print('A=%f'%A)
#CxCy
Cx=0
Cy=0
for i in range(len(data)-1):
	Cx+=(data[i][0]+data[i+1][0])*(data[i][0]*data[i+1][1]-data[i+1][0]*data[i][1])
	Cy+=(data[i][1]+data[i+1][1])*(data[i][0]*data[i+1][1]-data[i+1][0]*data[i][1])
Cx/=6*A
Cy/=6*A
print('Cx=%f'%Cx)
print('Cy=%f'%Cy)
#Area of surface
As = 0
for i in range(len(orgData)-1):
	# print(orgData[i])
	As+=(orgData[i][1]+orgData[i+1][1])*(math.sqrt((orgData[i][1]-orgData[i+1][1])**2+(orgData[i][0]-orgData[i+1][0])**2))
As+=orgData[0][1]**2
As+=orgData[-1][1]**2
As*=math.pi
print('As=%f'%As)
