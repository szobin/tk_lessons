# lesson 1a: bubbles
#   home task: 1) add drawing arcs and rectangles
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
    el_type = choice([1, 2, 2, 3])
    d = randint(2, size//6)
    g = d // 5
    # h = randint(1, int(size/7))
    x0 = randint(1, size-d)
    y0 = randint(g * 30, (g + 1) * 30)
    if el_type == 1:
        canvas.create_rectangle(x0, y0, x0+d, y0+d, fill=color)
    if el_type == 2:
        canvas.create_oval(x0, y0, x0+d, y0+d, fill=color)
    if el_type == 3:
        canvas.create_arc(x0, y0, x0+d, y0+d, fill=color)

    root.update()
    s.enter(0.1, 1, draw_elem)


def main():
    try:
        s.enter(0.1, 1, draw_elem)
        s.run()
        # root.mainloop()
    except Exception as exc:
        print(repr(exc))
        root.quit()


main()
