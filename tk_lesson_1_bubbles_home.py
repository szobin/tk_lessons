# lesson 1a: bubbles
#   home task: add drawing arcs and rectangles
#

from tkinter import Tk, Canvas
import sched
import time
from random import choice, randint

colors = ['aqua', 'blue', 'fuchsia', 'green', 'maroon', 'orange', 'pink', 'purple', 'red', 'yellow', 'violet',
          'indigo', 'chartreuse', 'lime', '#f55c4b']
s = sched.scheduler(time.time, time.sleep)
size = 600
root = Tk()
canvas = Canvas(root, width=size, height=size)
canvas.pack()


def draw_elem():
    color = choice(colors)
    el_type = choice([1, 2, 2, 2])
    w = randint(1, int(size/5))
    h = randint(1, int(size/7))
    x0 = randint(1, size-w)
    y0 = randint(1, size-h)
    if el_type == 1:
        canvas.create_rectangle(x0, y0, x0+w, y0+h, fill=color)
    if el_type == 2:
        canvas.create_oval(x0, y0, x0+w, y0+h, fill=color)
    if el_type == 3:
        canvas.create_arc(x0, y0, x0+w, y0+h, fill=color)

    root.update()
    s.enter(0.1, 1, draw_elem)


def main():
    try:
        s.enter(0.1, 1, draw_elem)
        s.run()
        root.mainloop()
    except Exception as exc:
        print(repr(exc))
        root.quit()


main()
