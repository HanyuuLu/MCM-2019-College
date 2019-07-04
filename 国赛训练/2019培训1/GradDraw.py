import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import csv
read = list()
x = list()
y = list()
z = list()

with open('fit3P2.csv', 'r') as fileRead:
    reader = csv.reader(fileRead)
    for i in reader:
        x.append(float(i[0]))
        z.append(float(i[2]))
        y.append(float(i[1]))
x = np.array(x)
y = np.array(y)
z = np.array(z)

# data = np.random.randint(0, 255, size=[40, 40, 40])
# x, y, z = data[0], data[1], data[2]
ax = plt.subplot(111, projection='3d')  # 创建一个三维的绘图工程 #  将数据点分成三部分画，在颜色上有区分度
ax.scatter(x, y, z, c='b')  # 绘制数据点
# fig = plt.figure()
# ax=Axes3D(fig)
# ax.plot_surface(x, y, z, cmap='rainbow')
# ax.scatter(x[10:20], y[10:20], z[10:20], c='r')
# ax.scatter(x[30:40], y[30:40], z[30:40], c='r')
ax.set_zlabel('Z')  # 坐标轴 ax.set_ylabel('Y')
ax.set_xlabel('X')
plt.show()
