# lesson 4: snake game:
#  - eating food
#  - growing
#  - score pane

import sched
import time
import random
import tkinter as tk

MX = MY = 10
PX = PY = 3
NX, NY = 30, 20
SCORE_HEIGHT = 40
CW = CH = 20

W = 2*MX + 2*PX + NX*CW
H = 2*MY + 2*PY + NY*CH

cx = NX // 2
cy = NY // 2
d = 1
snake_len = 4
stop = False
cells = []
food = []

window = tk.Tk()
window.title("Snake")
s = sched.scheduler(time.time, time.sleep)

canvas = tk.Canvas(window, width=W, height=H+SCORE_HEIGHT+MX, bg='white')
canvas.pack()


def get_x(ccx):
    return MX + PX + ccx*CW


def get_y(ccy):
    return MY + PY + ccy*CH


def draw_board():
    canvas.create_rectangle(MX, MY, W - MX, H - MY, fill="white")


def draw_pane():
    canvas.delete("pane")
    canvas.create_rectangle(MX, H, W - MX, H + SCORE_HEIGHT, fill="gray", tag="pane")
    yy = H+SCORE_HEIGHT // 2
    canvas.create_text(2*MX, yy, text="Score", anchor="w", fill="white", tag="pane")

    canvas.create_text(2*MX+100, yy, text=str(snake_len), anchor="e", fill="white", tag="pane")


def add_random_food():
    p = (random.randint(0, NX - 1), random.randint(0, NY - 1))
    while in_snake(p[0], p[1]):
        p = (random.randint(0, NX - 1), random.randint(0, NY - 1))
    draw_food(p)


def draw_food(p):
    food.append(p)
    ccx, ccy = p
    x, y = get_x(ccx), get_y(ccy)
    canvas.create_oval(x, y, x + CW, y + CH, fill="red", tag=f"f{ccx}x{ccy}")


def del_food(i):
    ccx, ccy = food[i]
    del food[i]
    canvas.delete(f"f{ccx}x{ccy}")


def draw_head():
    x, y = get_x(cx), get_y(cy)
    canvas.create_rectangle(x, y, x+CW, y+CH, fill="green", tag="head")


def hide_head():
    canvas.delete("head")


def draw_cell():
    x, y = get_x(cx), get_y(cy)
    cells.append((cx, cy))
    canvas.create_rectangle(x, y, x+CW, y+CH, fill="gray", tag=f"c{cx}x{cy}")


def hide_cell():
    ccx, ccy = cells[0]
    del cells[0]
    canvas.delete(f"c{ccx}x{ccy}")


def in_food(xx, yy):
    for i, p in enumerate(food):
        if p == (xx, yy):
            return i
    return -1


def in_snake(xx, yy):
    for i, p in enumerate(cells):
        if p[0] == xx and p[1] == yy:
            return True
    return False


def on_time():
    global cx, cy, cells, food, snake_len

    d_dict = {1: lambda ccx, ccy: (ccx, ccy - 1 if ccy > 0 else NY-1),
              2: lambda ccx, ccy: (ccx, (ccy + 1) % NY),
              3: lambda ccx, ccy: (ccx - 1 if ccx > 0 else NX-1, ccy),
              4: lambda ccx, ccy: ((ccx + 1) % NX, ccy)}
    if d in d_dict:
        hide_head()
        draw_cell()
        cx, cy = d_dict[d](cx, cy)

        draw_head()
        if len(cells) > snake_len:
            hide_cell()

        i = in_food(cx, cy)
        if i >= 0:
            snake_len += 4
            del_food(i)
            add_random_food()
            draw_pane()

        window.update()
    if not stop:
        s.enter(0.2, 1, on_time)
    return


def onkey(event):
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
    if stop:
        window.quit()
    stop = True


def main():
    window.bind('<Key>', onkey)
    window.protocol("WM_DELETE_WINDOW", on_closing)

    draw_board()
    draw_pane()
    add_random_food()
    draw_head()

    s.enter(0.2, 1, on_time)
    s.run()


main()
