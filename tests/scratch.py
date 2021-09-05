from typing import AsyncIterable
from matplotlib.colors import Colormap
import numpy as np
import matplotlib.image as mpimg
from matplotlib import pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import matplotlib.transforms as mtransforms
from math import pi, atan, sin, cos
from scipy.ndimage import rotate, shift


map1 = mpimg.imread('./images/chinokyoten1f_fixed.png')
map2 = mpimg.imread('./images/chinokyoten2f_fixed.png')
map3 = mpimg.imread('./images/chinokyoten3f_fixed.png')


fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')
# ax.plot([0, 0, 0], [0, 0, 10], [0, 0, 20], )

# translation and rotation of 1F

x, y = np.mgrid[0:map1.shape[0], 0:map1.shape[1]]
z = np.atleast_2d(0)

# prompt for user input on coordinates of Point 1 and Point 2
p1_1 = eval(input('Please enter Floor 1\'s Point 1 Coordinate in (x, y) form: '))
p1_2 = eval(input('Please enter Floor 1\'s Point 2 Coordinate in (x, y) form: '))

# p1_1, p1_2 = (2841, 2284), (2783, 2387)
newp1_2 = ((p1_2[0]-p1_1[0]), (p1_2[1] - p1_1[1]))
rot1 = -atan(newp1_2[1]/newp1_2[0])

xt = x - p1_1[0]
yt = y - p1_1[1]
zt = z

xtr = xt*cos(rot1) - yt*sin(rot1)
ytr = xt*sin(rot1) + yt*cos(rot1)
ztr = z

ax.plot_surface(xtr, ytr, z, facecolors=map1, shade=False, rstride=20, cstride=20)

# translation and rotation of 2F

x, y = np.mgrid[0:map2.shape[0], 0:map2.shape[1]]
z = np.atleast_2d(10)
p2_1 = eval(input('Please enter Floor 2\'s Point 1 Coordinate in (x, y) form: '))
p2_2 = eval(input('Please enter Floor 2\'s Point 2 Coordinate in (x, y) form: '))
# p2_1, p2_2 = (2063, 1211), (2123, 1264)
newp2_2 = ((p2_2[0]-p2_1[0]), (p2_2[1] - p2_1[1]))
rot2 = -atan(newp2_2[1]/newp2_2[0])

xt = x - p2_1[0]
yt = y - p2_1[1]
zt = z

xtr = xt*cos(rot2) - yt*sin(rot2)
ytr = xt*sin(rot2) + yt*cos(rot2)
ztr = z

ax.plot_surface(xtr, ytr, z, facecolors=map2, shade=False, rstride=20, cstride=20)

# translation and rotation of 3F

x, y = np.mgrid[0:map3.shape[0], 0:map3.shape[1]]
z = np.atleast_2d(20)
p3_1 = eval(input('Please enter Floor 3\'s Point 1 Coordinate in (x, y) form: '))
p3_2 = eval(input('Please enter Floor 3\'s Point 2 Coordinate in (x, y) form: '))
# p3_1, p3_2 = (693, 1462), (727, 1388)
newp3_2 = ((p3_2[0]-p3_1[0]), (p3_2[1] - p3_1[1]))
rot3 = -atan(newp3_2[1]/newp3_2[0])


xt = x - p3_1[0]
yt = y - p3_1[1]
zt = z

xtr = xt*cos(rot3) - yt*sin(rot3)
ytr = xt*sin(rot3) + yt*cos(rot3)
ztr = z

ax.plot_surface(xtr, ytr, z, facecolors=map3, shade=False, rstride=20, cstride=20)


# ax.set_xlim(-1000, 1000)
# ax.set_ylim(-1000, 1000)

# ax.view_init(azim=0, elev=90)
plt.show()