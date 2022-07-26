# Minesweeper with Object Oriented Programming
from tkinter import *
import settings
import utils

# Basic Window
root = Tk()
root.configure(bg="black")
root.geometry(f'{settings.WIDTH}x{settings.HEIGHT}')
root.title("Minesweeper Game")
root.resizable(False, False)

top_frame = Frame(
    root,
    bg="red",
    width=settings.WIDTH,
    height=utils.height_prct(25)
)
top_frame.place(x=0, y=0)

left_frame = Frame(
    root,
    bg="blue",
    width=utils.width_prct(25),
    height=utils.height_prct(75)
)
left_frame.place(x=0, y=180)

# Run the window
root.mainloop()
