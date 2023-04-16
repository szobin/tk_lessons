# lesson 3: cells game:
#   - cells moving
#   - change moving direction by keys

import sched
import time
import tkinter as tk

MX = MY = 5
NX, NY = 30, 20
CW = CH = 20
SCORE_HEIGHT = 40
W = 2*MX + NX*CW
H = 2*MY + NY*CH
snake_len = 4

x, y = NX // 2, NY // 2
d = 1
stop = False
cells = []

window = tk.Tk()
window.title("Snake")

s = sched.scheduler(time.time, time.sleep)

canvas = tk.Canvas(window, width=W, height=H+SCORE_HEIGHT, bg='white')
canvas.pack()


def draw_board():
    canvas.create_rectangle(MX, MY, MX + CW*NX, MY + CH*NY, fill="white")


def draw_head():
    canvas.create_rectangle(x, y, x + CW, y + CH, fill="green", tag="head")


def hide_head():
    canvas.delete("head")


def draw_cell():
    cells.append((x, y))
    canvas.create_rectangle(x, y, x + CW, y + CH, fill="gray", tag=f'cell{x}x{y}')


def hide_cell():
    xx, yy = cells[0]
    del cells[0]
    canvas.delete(f'cell{xx}x{yy}')


def on_time():
    global x, y
    d_dict = {1: lambda xx, yy: (xx, yy - CH if yy-CH > 0 else yy - 2*CH + NY*CH),
              2: lambda xx, yy: (xx, (yy + CH) % (NY*CH - CH)),
              3: lambda xx, yy: (xx - CW if xx - CW > 0 else xx - 2 * CW + NX*CW, yy),
              4: lambda xx, yy: ((xx + CW) % (NX*CW - CW), yy)}
    if d in d_dict:
        hide_head()
        draw_cell()
        x, y = d_dict[d](x, y)

        draw_head()
        if len(cells) > snake_len:
            hide_cell()

        window.update()
    if not stop:
        s.enter(0.2, 1, on_time)
    return


def on_key(event):
    global stop
    if event.keysym == 'Escape':
        stop = True
        return

    d_dict = {'Up': 1, 'Down': 2, 'Left': 3, 'Right': 4}

    global d
    if event.keysym in d_dict:
        d = d_dict[event.keysym]
    return


def on_closing():
    global stop
    stop = True


def main():
    window.bind('<Key>', on_key)
    window.protocol("WM_DELETE_WINDOW", on_closing)

    draw_head()

    s.enter(0.2, 1, on_time)
    s.run()


main()
