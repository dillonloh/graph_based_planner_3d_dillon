import tkinter as tk
import random


window = tk.Tk()

window.rowconfigure(0, minsize=50, weight=1)
window.columnconfigure(0, minsize=50, weight=1)

label = tk.Label(text='6-sided Dice Simulator')
number = tk.Label(text='1')

def roll_dice():
    new_number = random.randint(1, 6)
    number['text'] = f'{new_number}'
    return None

roll_button = tk.Button(text='Roll Dice', command=roll_dice)

label.grid(row=0, column=0, sticky='ew')
number.grid(row=1, column=0, sticky='ew')
roll_button.grid(row=2, column=0, sticky='ew')

window.mainloop()
