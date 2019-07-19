import matplotlib
import matplotlib.pyplot as plt
import numpy as np
import const
import math
delta = 0.05
# x = np.arange(
#     const.LONGITUDE_LOWER,
#     const.LONGITUDE_UPPER,
#     delta
# )
# y = np.arange(
#     const.LATITUDE_LOWER,
#     const.LATITUDE_UPPER,
#     delta
# )
x = np.arange(-4,4,
    delta
)
y = np.arange(-4,4,
    delta
)
X, Y = np.meshgrid(x, y)
# Z = math.sin(X)+math.sin(Y)
# Z = X + Y
Z = np.sin(X**2)+np.sin(Y**2)
fig, ax = plt.subplots()
# CS = ax.contour(X, Y, Z ,5)
# ax.clabel(CS, inline=True)
ax.contourf(X, Y, Z, 1000, cmap=plt.cm.jet)
ax.set_title('hanyuu\' s demo')

# plt.show()
plt.show()
