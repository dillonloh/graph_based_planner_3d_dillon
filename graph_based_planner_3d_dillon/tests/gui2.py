from tkinter import *
from tkinter.filedialog import askopenfilename

from PIL import Image, ImageTk


NO_OF_POINTS = 3
SET_NO = 1

root = Tk()

frame_btn = Frame(root, bd=2,)

frame_btn.grid_rowconfigure(0, weight=1)
frame_btn.grid_columnconfigure(0, weight=1)

label_btn = Label(master=frame_btn, text='Set coordinates of:')
label_btn.grid(row=0, column=0)

def set_number(button_no):
    global SET_NO
    SET_NO = button_no

button_dict = {}
button_no = {}

for i in range(1, NO_OF_POINTS+1):
    button_dict['button{}'.format(i)] = Button(master=frame_btn, text='Point {}'.format(i), command=lambda j=i: set_number(j))
    button_dict['button{}'.format(i)].grid(row=0, column=i)

frame_btn.pack()

frame = Frame(root, bd=2, relief=SUNKEN)

frame.grid_rowconfigure(0, weight=1)
frame.grid_columnconfigure(0, weight=1)

xscroll = Scrollbar(frame, orient=HORIZONTAL)
xscroll.grid(row=1, column=0, sticky=E+W)
yscroll = Scrollbar(frame)
yscroll.grid(row=0, column=1, sticky=N+S)

canvas = Canvas(frame, bd=0, xscrollcommand=xscroll.set, yscrollcommand=yscroll.set)
canvas.grid(row=0, column=0, sticky=N+S+E+W)

xscroll.config(command=canvas.xview)
yscroll.config(command=canvas.yview)    

frame.pack(fill=BOTH,expand=1)

#adding the image
File = askopenfilename(parent=root, initialdir="C:/",title='Choose an image.')
img = ImageTk.PhotoImage(Image.open(File))
canvas.create_image(0,0,image=img,anchor="nw")
canvas.config(scrollregion=canvas.bbox(ALL))


#function to be called when mouse is clicked
def printcoords(event):
    #outputting x and y coords to console
    canvas = event.widget
    x = canvas.canvasx(event.x)
    y = canvas.canvasy(event.y)
    print('Coordinates of point {} is ({},{})'.format(SET_NO, x, y))

#mouseclick event
canvas.bind("<Button 1>", printcoords)



root.title('3D Alignment of Floor Plans')
root.mainloop()
