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


if USERINPUT == True:
    # prompt for user input on coordinates of Point 1 and Point 2

    import tkinter as tk

    window = tk.Tk()

    # frame0 (titles)

    frame0 = tk.Frame()

    title1 = tk.Label(text='Please insert the coordinates of the points you wish to align for each floor.', master=frame0)
    title2 = tk.Label(text='Ensure that points 1 and 2 correspond to the same points for each floor.', master=frame0)

    frame0.pack(pady=10)

    title1.grid(row=0, column=0)
    title2.grid(row=1, column=0)

    # end frame0

    # frame1 (coordinates of floor 1)

    frame1 = tk.Frame()

    label_f1 = tk.Label(text="Floor 1's coordinates", master=frame1)

    label_f1p1 = tk.Label(text="Point 1", master=frame1)
    label_f1x1 = tk.Label(text='x', master=frame1)
    label_f1y1 = tk.Label(text='y', master=frame1)

    field_f1x1 = tk.Entry(master=frame1)
    field_f1y1 = tk.Entry(master=frame1)

    label_f1p2 = tk.Label(text='Point 2', master=frame1)
    label_f1x2 = tk.Label(text='x', master=frame1)
    label_f1y2 = tk.Label(text='y', master=frame1)

    field_f1x2 = tk.Entry(master=frame1)
    field_f1y2 = tk.Entry(master=frame1)

    frame1.pack()

    label_f1.grid(row=1, column=0, rowspan=2)

    label_f1p1.grid(row=0, column=1, columnspan=2)
    label_f1x1.grid(row=1, column=1)
    label_f1y1.grid(row=1, column=2)
    label_f1p2.grid(row=0, column=4, columnspan=2)
    label_f1x2.grid(row=1, column=4)
    label_f1y2.grid(row=1, column=5)

    field_f1x1.grid(row=2, column=1)
    field_f1y1.grid(row=2, column=2)
    field_f1x2.grid(row=2, column=4)
    field_f1y2.grid(row=2, column=5)

    # end frame1

    # start frame2
    frame2 = tk.Frame()

    label_f2 = tk.Label(text="Floor 2's coordinates", master=frame2)

    label_f2p1 = tk.Label(text="Point 1", master=frame2)
    label_f2x1 = tk.Label(text='x', master=frame2)
    label_f2y1 = tk.Label(text='y', master=frame2)

    field_f2x1 = tk.Entry(master=frame2)
    field_f2y1 = tk.Entry(master=frame2)

    label_f2p2 = tk.Label(text='Point 2', master=frame2)
    label_f2x2 = tk.Label(text='x', master=frame2)
    label_f2y2 = tk.Label(text='y', master=frame2)

    field_f2x2 = tk.Entry(master=frame2)
    field_f2y2 = tk.Entry(master=frame2)

    frame2.pack()

    label_f2.grid(row=1, column=0, rowspan=2)

    label_f2p1.grid(row=0, column=1, columnspan=2)
    label_f2x1.grid(row=1, column=1)
    label_f2y1.grid(row=1, column=2)
    label_f2p2.grid(row=0, column=4, columnspan=2)
    label_f2x2.grid(row=1, column=4)
    label_f2y2.grid(row=1, column=5)

    field_f2x1.grid(row=2, column=1)
    field_f2y1.grid(row=2, column=2)
    field_f2x2.grid(row=2, column=4)
    field_f2y2.grid(row=2, column=5)

    # end frame2

    # start frame3

    frame3 = tk.Frame()

    label_f3 = tk.Label(text="Floor 3's coordinates", master=frame3)

    label_f3p1 = tk.Label(text="Point 1", master=frame3)
    label_f3x1 = tk.Label(text='x', master=frame3)
    label_f3y1 = tk.Label(text='y', master=frame3)

    field_f3x1 = tk.Entry(master=frame3)
    field_f3y1 = tk.Entry(master=frame3)

    label_f3p2 = tk.Label(text='Point 2', master=frame3)
    label_f3x2 = tk.Label(text='x', master=frame3)
    label_f3y2 = tk.Label(text='y', master=frame3)

    field_f3x2 = tk.Entry(master=frame3)
    field_f3y2 = tk.Entry(master=frame3)


    frame3.pack()

    label_f3.grid(row=1, column=0, rowspan=2)

    label_f3p1.grid(row=0, column=1, columnspan=2)
    label_f3x1.grid(row=1, column=1)
    label_f3y1.grid(row=1, column=2)
    label_f3p2.grid(row=0, column=4, columnspan=2)
    label_f3x2.grid(row=1, column=4)
    label_f3y2.grid(row=1, column=5)

    field_f3x1.grid(row=2, column=1)
    field_f3y1.grid(row=2, column=2)
    field_f3x2.grid(row=2, column=4)
    field_f3y2.grid(row=2, column=5)

    # end frame3

    frame4 = tk.Frame()

    def submit():

        global p1_1, p1_2, p2_1, p2_2, p3_1, p3_2

        f1x1 = field_f1x1.get()
        f1y1 = field_f1y1.get()
        f1x2 = field_f1x2.get()
        f1y2 = field_f1y2.get()
        p1_1 = (int(f1x1), int(f1y1))
        p1_2 = (int(f1x2), int(f1y2))

        f2x1 = field_f2x1.get()
        f2y1 = field_f2y1.get()
        f2x2 = field_f2x2.get()
        f2y2 = field_f2y2.get()
        p2_1 = (int(f2x1), int(f2y1))
        p2_2 = (int(f2x2), int(f2y2))

        f3x1 = field_f3x1.get()
        f3y1 = field_f3y1.get()
        f3x2 = field_f3x2.get()
        f3y2 = field_f3y2.get()
        p3_1 = (int(f3x1), int(f3y1))
        p3_2 = (int(f3x2), int(f3y2))

        window.destroy()
        return None


    submit_button = tk.Button(text='Confirm Coordinates', command=submit, master=frame4)

    frame4.pack(pady=15)

    submit_button.grid(row=0, column=0)

    window.title('3D Alignment of Floor Plans')
    window.mainloop()

else:
    p1_1, p1_2 = (2841, 2284), (2783, 2387)
    p2_1, p2_2 = (2063, 1211), (2123, 1264)
    p3_1, p3_2 = (693, 1462), (727, 1388)


fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')
ax.plot([0, 0, 0], [0, 0, 10], [0, 0, 20], )

# translation and rotation of 1F

x, y = np.mgrid[0:map1.shape[0], 0:map1.shape[1]]
z = np.atleast_2d(0)


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