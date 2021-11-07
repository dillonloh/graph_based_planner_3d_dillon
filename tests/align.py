from typing import AsyncIterable
from matplotlib.colors import Colormap
import numpy as np
import matplotlib.image as mpimg
from matplotlib import pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import matplotlib.transforms as mtransforms
from math import floor, pi, atan, sin, cos, sqrt, acos
from numpy.lib.function_base import average
from scipy.ndimage import rotate, shift
from sklearn import linear_model
from scipy.optimize import curve_fit, fmin




CALIBRATION_METHOD = 'AVERAGE_ANGLE' # methods available are 'AVERAGE_ANGLE' or 'MIN_SQUARES'


map1 = mpimg.imread('./images/chinokyoten1f_marked.png')
map2 = mpimg.imread('./images/chinokyoten2f_marked.png')
map3 = mpimg.imread('./images/chinokyoten3f_marked.png')

maps = [map1, map2, map3]


f1 = [[2841, 2284], [2783, 2387], [1911, 1891], [2002, 1701]]
f2 = [[2063, 1211], [2123, 1264], [1614, 1911], [1477, 1803]]
f3 = [[693, 1462], [727, 1388], [1463, 1672], [1393, 1835]]


floor_points = [f1, f2, f3]

# translation of points

translated_floor_points = floor_points
translation_amounts = []

for f in translated_floor_points:
    translation_x = f[0][0]
    translation_y = f[0][1]
    translation_amounts.append([translation_x, translation_y])
    for point in f:
        point[0] -= translation_x
        point[1] -= translation_y

# rotating of points

def find_len(point1, point2):
    """find length using pythagoras theorem"""
    return sqrt((point2[1]-point1[1])**2 + (point2[0]-point1[0])**2)


def find_angle(point1, point2):
    """find angle between 2 points"""
    origin = (0, 0)
    A = find_len(origin, point1)
    B = find_len(point1, point2)
    C = find_len(origin, point2)

    angle = acos((A**2 + C**2 - B**2)/(2*A*C))

    return angle


all_angles_by_floor = []

for i in range(1, 4): # number of points
    angles = []    
    for j in range(1, 3): # number of floors 
        point1 = f1[i]
        point2 = floor_points[j][i]
        angles.append(find_angle(f1[i], floor_points[j][i]))

    all_angles_by_floor.append(angles)

f2_angles = [all_angles_by_floor[0][0], all_angles_by_floor[1][0], all_angles_by_floor[2][0]]


# print(all_angles_by_floor)
# print('2F vs 1F', f2_angles)



# rotation of points (we only rotate the 2F and above)


def translation(trans_x, trans_y, x, y):
    """translation of point (x, y) by (trans_x, trans_y)"""
    xt = x + trans_x
    yt = y + trans_y
    return xt, yt


def rotation(angle, x, y):
    """rotation of point (x, y) about origin by angle"""
    xr = x*cos(angle) - y*sin(angle)
    yr = x*sin(angle) + y*cos(angle)
    return xr, yr

if CALIBRATION_METHOD == 'AVERAGE_ANGLE':

    # initialise plot
    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')

    # find avg rotation angles
    rot_angles = [0] # initialise with 0 rotation angle for 1st floor

    for i in range(2): # no of floors - 1 cause exclude 1st floor
        sum = 0
        for j in range(3): # no of points - 1 cause excluding origin point after translation
            sum += all_angles_by_floor[j][i]
        average_rot = sum/3 # no of angles summed up (no of points - 1)
    
        rot_angles.append(average_rot)
        
            

    # translate and rotate

    for i in range(2):
        x, y = np.mgrid[0:maps[i].shape[0], 0:maps[i].shape[1]]
        z = np.atleast_2d(i*10)
        
        xt, yt = translation(-translation_amounts[i][0], -translation_amounts[i][1], x, y)
        xtr, ytr = rotation(rot_angles[i], xt, yt)
        ax.plot_surface(xtr, ytr, z, facecolors=maps[i], shade=False, rstride=20, cstride=20)


    plt.show()

elif CALIBRATION_METHOD == 'MIN_SQUARES':
    NO_OF_ANGLES = 100
    rot_angles = np.linspace(0,2*pi, NO_OF_ANGLES)



    # generating all rotated points for each angle for 2nd floor

    f2_rotated_points = []

    for angle in rot_angles:
        by_angles = []
        for point in translated_floor_points[1]:
            rot_point = []
            x, y = rotation(angle, point[0], point[1])
            rot_point.append(x)
            rot_point.append(y)
            by_angles.append(rot_point)
        f2_rotated_points.append(by_angles)
        
    # print(f2_rotated_points)

    # finding distance between corresponding points
    f2_dist = []
    translated_f1 = translated_floor_points[0]

    for i in range(NO_OF_ANGLES): # no of angles in rot_angles
        sum = 0
        for j in range(4): # no of points
            p2pdist = find_len(translated_f1[j], f2_rotated_points[i][j])
            sum += p2pdist

        f2_dist.append(sum)



    # fitting model
    
    def objective(theta, a, phi):
        return np.sqrt((2*a**2)*(1-np.cos(theta+phi)))

    popt, pcov = curve_fit(objective, rot_angles, f2_dist, maxfev=5000)

    def fitted_model(theta):
        popt, pcov = curve_fit(objective, rot_angles, f2_dist, maxfev=5000)
        a = popt[0]
        phi = popt[1]
        return np.sqrt((2*a**2)*(1-np.cos(theta+phi)))

    # find minimum of fitted model
    min = fmin(fitted_model, 0) # this is our rotation angle
    rotation_angles = [0, min]

    # plotting

    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')

    for i in range(2):
        x, y = np.mgrid[0:maps[i].shape[0], 0:maps[i].shape[1]]
        z = np.atleast_2d(i*10)
        
        xt, yt = translation(-translation_amounts[i][0], -translation_amounts[i][1], x, y)
        xtr, ytr = rotation(rotation_angles[i], xt, yt)
        ax.plot_surface(xtr, ytr, z, facecolors=maps[i], shade=False, rstride=20, cstride=20)

    plt.show()








    # for angle in rot_angles:
        
    #     rotated_points = [translated_floor_points[0]] # initalise with the first floor points because we wont rotate them
   
    #     for i in range(1,3):
    #         floor = []
    #         for point in translated_floor_points[i]:
    #             rot_point = []
    #             x, y = rotation(angle, point[0], point[1])
    #             rot_point.append(x)
    #             rot_point.append(y)
    #             floor.append(rot_point)
    #         rotated_points.append(floor)

    #     all_rotated_points.append(rotated_points)

    # # calculate distances
    # all_norms = []
    # for angle in range(len(rot_angles)):
    #     norm_by_angle = []
    #     for floor in range(1, 3):
    #         norm_by_floor = []
    #         for point in range(1, 4):
    #             norm = find_len(all_rotated_points[angle][floor][point], all_rotated_points[0][0][point])
    #             print(norm)



            

