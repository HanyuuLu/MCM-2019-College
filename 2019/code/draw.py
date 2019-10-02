import matplotlib
import matplotlib.pyplot as plt
import json
import datetime
import time
with open('./log.json', 'r') as r:
    data = json.load(r)
# srcData = data['乘客运量统计']
# x = list(range(24))
# y = [x/2 for x in srcData]
# print(x)
# print(y)

# x = list(range(24))
# y = [0]*24
# srcData = data['各列表历史记录']
# for i in srcData:
#     # print(int(i['time'][-8:-6]))
#     y[int(i['time'][-8:-6])] += int(i['passenger'])
# for i in range(24):
#     y[i] /= 60
# yy = [322, 424, 508, 480, 330,
#       108, 0, 0, 0, 0,
#       0, 69, 80, 81, 102,
#       112, 98, 78, 98, 102,
#       98, 89, 102, 500
#       ]

x = [0, 0.1, 0.2, 0.3, 0.4, 0.5, 0.6]
# y = [1, 0.86, 0.78, 0.73, 0.62, 0.48, 0.39]
yy = [1, 0.92, 0.87, 0.79, 0.69, 0.58, 0.49]
y = [5, 6.23, 7.67, 9.02, 11.23, 15.33, 19.42]

# a = [-5, 0, 5, 10]
# b = [0, 0, 5, 5]
plt.rcParams['font.sans-serif'] = ['SimHei']  # 用来正常显示中文标签
plt.rcParams['axes.unicode_minus'] = False  # 用来正常显示负号
plt.grid(True, linestyle="-.", color="r", linewidth="3")
plt.title("蓄车池数目估计错误对平均等待时间的影响")
plt.tick_params(axis="both", which="major")
plt.grid(True, linestyle="-", color="gray", linewidth="1")
plt.xlabel("错误率")
plt.ylabel("平均等待时间(min)")
# plt.plot(x, y, label='缺失抵达航班信息')
plt.plot(x, y)
# plt.plot(x, yy, label='缺失出发航班信息')
plt.legend(loc='upper right')
plt.show()
