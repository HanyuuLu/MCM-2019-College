import matplotlib.pyplot as plt
import matplotlib.image as mpimg
import numpy as np

# 24° 0'0.00"北 114°59'60.00"东
# 22° 0'0.00"北112° 0'0.00"东

img = mpimg.imread('res/map.png')
upN = 24
lowN = 22
upE = 112
lowE = 115
# plt.imshow((lowE,lowN),img)
plt.plot(img)
plt.show()
