#  导入相应的包

import matplotlib.pylab as plt
# import numpy as np
import scipy  
import scipy.cluster.hierarchy as sch
from scipy.cluster.vq import kmeans, vq, whiten

# 生成待聚类的数据点,这里生成了20个点,每个点4维:\
points = scipy.randn(20, 4)

# 1. 层次聚类
# 生成点与点之间的距离矩阵,这里用的欧氏距离:
disMat = sch.distance.pdist(points, 'euclidean')
# 进行层次聚类:
Z = sch.linkage(disMat, method='average')
# 将层级聚类结果以树状图表示出来并保存为plot_dendrogram.png
P = sch.dendrogram(Z)
plt.savefig('plot_dendrogram.png')
# 根据linkage matrix Z得到聚类结果:
cluster = sch.fcluster(Z, t=2, criterion='inconsistent')

print("Original cluster by hierarchy clustering:\n", cluster)

# 2. k-means聚类
# 将原始数据做归一化处理
data = whiten(points)

# 使用kmeans函数进行聚类,输入第一维为数据,第二维为聚类个数k.
# 有些时候我们可能不知道最终究竟聚成多少类,一个办法是用层次聚类的结果进行初始化.当然也可以直接输入某个数值.
# k-means最后输出的结果其实是两维的,第一维是聚类中心,第二维是损失distortion,我们在这里只取第一维,所以最后有个[0]
centroid = kmeans(data, max(cluster))[0]

# 使用vq函数根据聚类中心对所有数据进行分类,vq的输出也是两维的,[0]表示的是所有数据的label
label = vq(data, centroid)[0]

print("Final clustering by k-means:\n", label)
