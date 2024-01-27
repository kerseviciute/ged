from tkinter import *
from tkinter.ttk import *

window = Tk()

#
# Window setup
#
window.title('Generalized Eigenvalue Decomposition')

window.resizable(False, False)

window_width = 1200
window_height = 800

screen_width = window.winfo_screenwidth()
screen_height = window.winfo_screenheight()

x_coordinate = int((screen_width/2) - (window_width/2))
y_coordinate = int((screen_height/2) - (window_height/2))

window.geometry(f"{window_width}x{window_height}+{x_coordinate}+{y_coordinate}")



window.mainloop()
