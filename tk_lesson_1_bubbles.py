# lesson 1: bubbles
#   - make board
#   - draw random color bubbles
#
import random as rm
import tkinter as tk
import time as tm

SIZE = 600
COLORS = ['aqua', 'blue', 'fuchsia', 'green', 'maroon', 'orange', 'pink',
          'purple', 'red', 'yellow', 'violet', 'indigo', 'chartreuse',
          'lime', '#f55c4b']

root = tk.Tk()
canvas = tk.Canvas(root, width=SIZE, height=SIZE)
canvas.pack()

try:
    while True:
        color = rm.choice(COLORS)
        d = rm.randint(10, SIZE//5)
        xc = rm.randint(0, SIZE)
        yc = rm.randint(0, SIZE)
        canvas.create_oval(xc, yc, xc+d, yc+d, fill=color)
        root.update()
        tm.sleep(0.1)
except Exception as exc:
    print(repr(exc))
    root.quit()
