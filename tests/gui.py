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


frame4 = tk.Frame()


def submit():
    f1x1 = field_f1x1.get()
    f1y1 = field_f1y1.get()
    f1x2 = field_f1x2.get()
    f1y2 = field_f1y2.get()


    f2x1 = field_f2x1.get()
    f2y1 = field_f2y1.get()
    f2x2 = field_f2x2.get()
    f2y2 = field_f2y2.get()

    f3x1 = field_f3x1.get()
    f3y1 = field_f3y1.get()
    f3x2 = field_f3x2.get()
    f3y2 = field_f3y2.get()

    return None

submit_button = tk.Button(text='Confirm Coordinates', command=submit, master=frame4)

frame4.pack(pady=15)

submit_button.grid(row=0, column=0)


window.title('3D Alignment of Floor Plans')
window.mainloop()

