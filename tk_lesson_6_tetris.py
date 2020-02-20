# - draw board and figure
# - move figure down
# hometask: - move figure left and right

import tkinter as tk
import sched as sd
import time as tm

# margins
MX = 10
MY = 10

# padding
PX = 4
PY = 4

# cells
CW = 20
CH = 20

CELLS_X = 12
CELLS_Y = 30

# velocity
TIME_VEL = 0.4

stop = False
root = tk.Tk()
s = sd.scheduler(tm.time, tm.sleep)

canvas = tk.Canvas(root,
                   width=CELLS_X*CW + 2*MX + PX,
                   height=CELLS_Y*CH + 2*MY + PY,
                   bg='white')
canvas.pack()


def get_x(cx):
    return cx*CW + MX + PX


def get_y(cy):
    return cy*CH + MY + PX


class Figure:
    cells = [(0, 0), (0, 1), (0, 2), (0, 3)]

    def __init__(self, cx, cy):
        self.p = (cx, cy)

    def hide_cell(self, cx, cy):
        x = get_x(cx + self.p[0])
        y = get_y(cy + self.p[1])
        canvas.create_rectangle(x, y, x+CW, y+CH, fill="white", outline="white")

    def show_cell(self, cx, cy):
        x = get_x(cx + self.p[0])
        y = get_y(cy + self.p[1])
        canvas.create_rectangle(x, y, x+CW, y+CH, fill="blue", outline="black")

    def hide(self):
        for cx, cy in self.cells:
            self.hide_cell(cx, cy)

    def show(self):
        for cx, cy in self.cells:
            self.show_cell(cx, cy)

    def check(self, p):
        for x, y in self.cells:
            if y+p[1] >= CELLS_Y:
                return False
            if x + p[0] >= CELLS_X:
                return False
            if x + p[0] < 0:
                return False
        return True

    def down(self):
        p_new = (self.p[0], self.p[1]+1)
        if not self.check(p_new):
            return False

        self.hide()
        self.p = p_new
        self.show()
        return True

    def shift(self, d):
        p_new = (self.p[0] + d, self.p[1])
        if not self.check(p_new):
            return False
        self.hide()
        self.p = p_new
        self.show()
        return True


f = Figure(3, 0)


def draw_board():
    canvas.create_rectangle(MX, MY,
                            get_x(CELLS_X)+PX,
                            get_y(CELLS_Y)+PY, fill="white")


def on_key(event):
    global stop
    if event.keysym == 'Escape':
        stop = True
        return

    elif event.keysym == 'Left':
        f.shift(-1)
    elif event.keysym == 'Right':
        f.shift(1)


def on_close():
    global stop
    if stop:
        root.quit()
    stop = True


def move():
    global f
    f.down()

    root.update()
    if not stop:
        s.enter(TIME_VEL, 1, move)
    return


def main():
    draw_board()
    root.bind('<Key>', on_key)
    root.protocol("WM_DELETE_WINDOW", on_close)

    s.enter(TIME_VEL, 1, move)
    s.run()


main()
