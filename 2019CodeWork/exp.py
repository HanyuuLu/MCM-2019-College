# 这是所有订单中按照支付小时数绘制的直方图

import matplotlib.pyplot as plt
import numpy as np
import matplotlib.ticker as mtick
from matplotlib.font_manager import FontProperties
# font = FontProperties(fname=r"c:\windows\fonts\simsun.ttc", size=14)
a = [1228.3, 3.38, 63.8, 0.07, 0.16, 6.74, 1896.18]  # 数据
b = [0.12, -12.44, 1.82, 16.67, 6.67, -6.52, 4.04]
l = [i for i in range(7)]

plt.rcParams['font.sans-serif']=['SimHei'] #用来正常显示中文标签

fmt = '%.2f%%'
yticks = mtick.FormatStrFormatter(fmt)  # 设置百分比形式的坐标轴
lx = [u'粮食', u'棉花', u'油料', u'麻类', u'糖料', u'烤烟', u'蔬菜']

fig = plt.figure()
ax1 = fig.add_subplot(111)
ax1.plot(l, b, 'or-', label=u'增长率')
ax1.yaxis.set_major_formatter(yticks)
for i, (_x, _y) in enumerate(zip(l, b)):
    plt.text(_x, _y, b[i], color='black', fontsize=10,)  # 将数值显示在图形上
ax1.legend(loc=1)
ax1.set_ylim([-20, 30])
ax1.set_ylabel('增长率')
plt.legend(prop={'family': 'SimHei', 'size': 8})  # 设置中文
ax2 = ax1.twinx()  # this is the important function
plt.bar(l, a, alpha=0.3, color='blue', label=u'产量')
ax2.legend(loc=2)
ax2.set_ylim([0, 2500])  # 设置y轴取值范围
plt.legend(prop={'family': 'SimHei', 'size': 8}, loc="upper left")
plt.xticks(l, lx)
plt.show()
