from typing import AsyncIterable
from matplotlib.colors import Colormap
import numpy as np
import matplotlib.image as mpimg
from matplotlib import pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import matplotlib.transforms as mtransforms
from math import pi, atan, sin, cos
from scipy.ndimage import rotate, shift

# Initialisation Parameters

USERINPUT = False # if True, allow user to manually set point1 and point2 coordinates


map1 = mpimg.imread('./images/chinokyoten1f_fixed.png')
map2 = mpimg.imread('./images/chinokyoten2f_fixed.png')
map3 = mpimg.imread('./images/chinokyoten3f_fixed.png')

NO_FLOORS = 3
MAP_IMAGES = [map1, map2, map3]



fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')

for i in range(NO_FLOORS): # set 2 for faster load
    x, y = np.mgrid[0:MAP_IMAGES[i].shape[0], 0:MAP_IMAGES[i].shape[1]]
    z = np.atleast_2d(i*10)

    ax.plot_surface(x, y, z, facecolors=MAP_IMAGES[i], shade=False, rstride=20, cstride=20)

plt.show()
