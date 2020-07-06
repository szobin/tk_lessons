# lesson #6
# tetris #1

# - board and figure classes
# - move figure down
# hometask: - move figure left and right

import tkinter as tk
import sched as sd
import time as tm

# margins
MX = MY = 10

# padding
PX = PY = 4

# cells
CW = CH = 20

CELLS_X = 12
CELLS_Y = 30


def get_x(cx):
    return cx*CW + MX + PX


def get_y(cy):
    return cy*CH + MY + PX


class Board:
    def __init__(self, canvas):
        self.canvas = canvas

    def draw(self):
        self.canvas.create_rectangle(MX, MY, get_x(CELLS_X)+PX, get_y(CELLS_Y)+PY, fill="white")


class Figure:
    cells = [(0, 0), (0, 1), (0, 2), (0, 3)]

    def __init__(self, canvas):
        self.canvas = canvas
        self.p = (5, 0)

    def show_cell(self, cx, cy):
        x = get_x(cx + self.p[0])
        y = get_y(cy + self.p[1])
        self.canvas.create_rectangle(x, y, x+CW, y+CH, fill="blue", outline="black", tag="figure")

    def hide(self):
        self.canvas.delete("figure")

    def show(self):
        for cx, cy in self.cells:
            self.show_cell(cx, cy)

    def check(self, p):
        px, py  = p
        for x, y in self.cells:
            if y+py >= CELLS_Y:
                return False
            # HW:
            if x + px >= CELLS_X:
                return False
            if x + py < 0:
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

    # HW:
    def shift(self, d):
        p_new = (self.p[0] + d, self.p[1])
        if not self.check(p_new):
            return False
        self.hide()
        self.p = p_new
        self.show()
        return True


stop = False

window = tk.Tk()
window.title("Tetris")

s = sd.scheduler(tm.time, tm.sleep)

c = tk.Canvas(window,
              width=CELLS_X*CW + 2*MX + PX,
              height=CELLS_Y*CH + 2*MY + PY,
              bg='white')
c.pack()

board = Board(c)
figure = Figure(c)


def on_key(event):
    if event.keysym == 'Left':
        figure.shift(-1)
    if event.keysym == 'Right':
        figure.shift(1)


def on_time():
    figure.down()

    window.update()
    if not stop:
        s.enter(0.25, 1, on_time)
    return


def on_close():
    global stop
    stop = True


def main():
    window.protocol("WM_DELETE_WINDOW", on_close)
    window.bind('<Key>', on_key)

    board.draw()
    figure.show()

    s.enter(0.25, 1, on_time)
    s.run()


main()
