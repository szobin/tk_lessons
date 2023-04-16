# lesson #8
# tetris #3

# - board: copy_figure, in_cells
# - figure: shift, rotate, respawn
# home task: - add figure 3, 4, 5, 6, 7

import tkinter as tk
import sched as sd
import time as tm
import random

BLOCK_COLORS = ['aqua', 'blue', 'fuchsia', 'green', 'maroon', 'orange', 'pink', 'purple']

BLOCK_1 = [(0, 0), (0, 1), (0, 2), (0, 3)]
BLOCK_2 = [(0, 0), (0, 1), (0, 2), (1, 2)]
BLOCK_3 = [(0, 0), (0, 1), (1, 1), (1, 0)]
BLOCK_4 = [(0, 0), (1, 0), (2, 0), (2, 1)]
BLOCK_TYPES = [BLOCK_1, BLOCK_2, BLOCK_3, BLOCK_4]

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
f = None

canvas = tk.Canvas(root,
                   width=CELLS_X*CW + 2*MX + PX,
                   height=CELLS_Y*CH + 2*MY + PY,
                   bg='white')
canvas.pack()


def get_x(cx):
    return cx*CW + MX + PX


def get_y(cy):
    return cy*CH + MY + PX


def rotate_cells(cells):
    ax, ay = cells[0]
    cells_r = [(ax, ay)]
    for i in range(1, len(cells)):
        c = cells[i]
        bx, by = c[0] - ax, c[1] - ay
        cx, cy = ax - by, ay + bx
        cells_r.append((cx, cy))
    return cells_r


class BoardCell:

    def __init__(self, x, y, color):
        self.x = x
        self.y = y
        self.color = color


class BoardMap:

    def __init__(self, nx=CELLS_X, ny=CELLS_Y):
        self.nx = nx
        self.ny = ny
        self.cells = []

    @staticmethod
    def draw_cell(c):
        x = get_x(c.x)
        y = get_y(c.y)
        canvas.create_rectangle(x, y, x+CW, y+CH, fill=c.color, outline="black")

    def draw(self):
        canvas.create_rectangle(MX, MY,
                                get_x(self.nx) + PX,
                                get_y(self.ny) + PY, fill="white")
        for c in self.cells:
            self.draw_cell(c)

    def add_figure(self, p, cells, color):
        for cx, cy in cells:
            self.cells.append(BoardCell(cx + p[0],
                                        cy + p[1],
                                        color))
        self.draw()

    def in_cells(self, cx, cy):
        for c in self.cells:
            if (c.x == cx) and (c.y == cy):
                return True
        return False


board = BoardMap()


class Figure:

    def __init__(self, cx, cy):
        self.color = random.choice(BLOCK_COLORS)
        self.cells = random.choice(BLOCK_TYPES)
        self.p = (cx, cy)

    def hide_cell(self, cx, cy):
        x = get_x(cx + self.p[0])
        y = get_y(cy + self.p[1])
        canvas.create_rectangle(x, y, x+CW, y+CH, fill="white", outline="white")

    def show_cell(self, cx, cy):
        x = get_x(cx + self.p[0])
        y = get_y(cy + self.p[1])
        canvas.create_rectangle(x, y, x+CW, y+CH, fill=self.color, outline="black")

    def hide(self):
        for cx, cy in self.cells:
            self.hide_cell(cx, cy)

    def show(self):
        for cx, cy in self.cells:
            self.show_cell(cx, cy)

    def check(self, p, cells=None):
        check_cells = cells if cells is not None else self.cells
        for x, y in check_cells:
            xx, yy = x + p[0], y+p[1]
            if (yy < 0) or (yy >= CELLS_Y):
                return False
            if (xx < 0) or (xx >= CELLS_X):
                return False
            if board.in_cells(xx, yy):
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

    def rotate(self):
        cells_new = rotate_cells(self.cells)
        if not self.check(self.p, cells_new):
            return False
        self.hide()
        self.cells = cells_new
        self.show()


def new_figure():
    global f
    f = Figure(5, 0)


def on_key(event):
    global stop
    if event.keysym == 'Escape':
        stop = True
        return

    elif event.keysym == 'Left':
        f.shift(-1)
    elif event.keysym == 'Right':
        f.shift(1)
    elif event.keysym == 'Up':
        f.rotate()


def on_close():
    global stop
    if stop:
        root.quit()
    stop = True


def on_time():
    if not f.down():
        board.add_figure(f.p, f.cells, f.color)
        new_figure()

    root.update()
    if not stop:
        s.enter(TIME_VEL, 1, on_time)
    return


def main():
    board.draw()
    new_figure()
    root.bind('<Key>', on_key)
    root.protocol("WM_DELETE_WINDOW", on_close)

    # f.down()

    s.enter(TIME_VEL, 1, on_time)
    s.run()


main()
