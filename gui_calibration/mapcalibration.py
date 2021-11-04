from typing import AsyncIterable
from matplotlib.colors import Colormap
import numpy as np
import matplotlib.image as mpimg
from matplotlib import pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import matplotlib.transforms as mtransforms
from math import pi, atan, sin, cos
from scipy.ndimage import rotate, shift
import pickle


print('Nice')

with open('gui_calibration\shared.pkl', 'rb') as fp:
    shared = pickle.load(fp)


NO_FLOORS = shared[-2]
NO_OF_POINTS = shared[-1]

MAP_IMAGES = []
surface_list = []

for i in range(NO_FLOORS):
    map_path = shared[i]['img']
    MAP_IMAGES.append(mpimg.imread(map_path))
    surface_list.append([0, 0, i*10])


fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')


for i, map in zip(range(NO_FLOORS), MAP_IMAGES):
    x, y = np.mgrid[0:map.shape[0], 0:map.shape[1]]
    z = np.atleast_2d(i*10)
    print(z)
    ax.plot_surface(x, y, z, facecolors=map, shade=False, rstride=20, cstride=20)


########### TBC: MIN SQUARES CALIBRATION ###########

# ax.set_xlim(-1000, 1000)
# ax.set_ylim(-1000, 1000)

# ax.view_init(azim=0, elev=90)
plt.show()