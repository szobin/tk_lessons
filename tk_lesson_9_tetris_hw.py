# lesson #9
# tetris #4
# - game over, reset game, drop figure
# home task: assign both color and block

import tkinter as tk
import sched as sd
import time as tm
import random

BLOCK_COLORS = ['blue', 'fuchsia', 'green', 'maroon']

BLOCK_1 = [(0, 0), (0, 1), (0, 2), (0, 3)]
BLOCK_2 = [(0, 0), (0, 1), (0, 2), (1, 2)]
BLOCK_3 = [(0, 0), (0, 1), (1, 1), (1, 0)]
BLOCK_4 = [(0, 0), (1, 0), (2, 0), (2, 1)]

# HW:
BLOCK_TYPES = [(BLOCK_1, 'blue'),  (BLOCK_2, 'green'),
               (BLOCK_3, 'fuchsia'), (BLOCK_4, 'maroon')]

# margins
MX = MY = 10

# padding
PX = PY = 4

# cells
CW = CH = 30

CELLS_X = 12
CELLS_Y = 30

# velocity
TIME_VEL = 0.4


def get_x(cx):
    return cx*CW + MX + PX


def get_y(cy):
    return cy*CH + MY + PX


def rotate_cells(cells):
    ax, ay = cells[0]
    cells_r = [(ax, ay)]
    for i in range(1, len(cells)):
        cx, cy = cells[i]
        bx, by = cx - ax, cy - ay
        cx, cy = ax - by, ay + bx
        cells_r.append((cx, cy))
    return cells_r


class Board:

    def __init__(self, canvas):
        self.canvas = canvas
        self.cells = []

    def draw_cell(self, cx, cy, color):
        xx = get_x(cx)
        yy = get_y(cy)
        self.canvas.create_rectangle(xx, yy, xx+CW, yy+CH,
                                     fill=color, outline="black", tag="cells{}x{}".format(cx, cy))

    def draw(self):
        self.canvas.create_rectangle(MX, MY,
                                     get_x(CELLS_X) + PX,
                                     get_y(CELLS_Y) + PY, fill="white")
        for cx, cy, color in self.cells:
            self.draw_cell(cx, cy, color)

    def copy_figure(self, p, cells, color):
        px, py = p
        for cx, cy in cells:
            self.cells.append((cx + px, cy + py, color))
            self.draw_cell(cx + px, cy + py, color)

    def reset_game(self):
        while len(self.cells) > 0:
            cx, cy, color = self.cells[0]
            self.canvas.delete("cells{}x{}".format(cx, cy))
            del self.cells[0]

    def in_cells(self, px, py):
        for cx, cy, color in self.cells:
            if (px == cx) and (py == cy):
                return True
        return False


class Figure:
    color = None
    cells = None
    p = (0, 0)

    def __init__(self, canvas, board):
        self.canvas = canvas
        self.board = board
        self.respawn()

    def respawn(self):
        # HW:
        self.cells, self. color = random.choice(BLOCK_TYPES)
        px = random.randint(1, CELLS_X - 2)
        self.p = (px, 0)
        return self.check(self.p)

    def show_cell(self, cx, cy):
        px, py = self.p
        xx = get_x(cx + px)
        yy = get_y(cy + py)
        self.canvas.create_rectangle(xx, yy, xx+CW, yy+CH, fill=self.color, outline="black", tag="figure")

    def hide(self):
        self.canvas.delete("figure")

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
            if self.board.in_cells(xx, yy):
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


window = tk.Tk()
window.title("Tetris")
s = sd.scheduler(tm.time, tm.sleep)
restart_var = tk.IntVar()
stop = False

c = tk.Canvas(window,
              width=CELLS_X*CW + 2*MX + PX,
              height=CELLS_Y*CH + 2*MY + PY,
              bg='white')
c.pack()
b = Board(c)
figure = Figure(c, b)


def on_key(event):
    # to prevent move figure in game-over mode
    if stop:
        return

    elif event.keysym == 'Left':
        figure.shift(-1)
    elif event.keysym == 'Right':
        figure.shift(1)
    elif event.keysym == 'Up':
        figure.rotate()
    elif event.keysym == 'Down':
        drop_figure()


def on_close():
    global stop
    if stop:
        window.quit()
    stop = True


def show_game_over(canvas):
    canvas.create_rectangle(get_x(CELLS_X // 2 - 6), get_y(CELLS_Y // 2 - 3),
                            get_x(CELLS_X // 2 + 6), get_y(CELLS_Y // 2 + 3),
                            fill="gray", tag="game_over")
    xx = get_x(CELLS_X) // 2 + CW // 2
    yy = get_y(CELLS_Y) // 2 - CH
    canvas.create_text(xx, yy, font=("Purisa", 22),
                       text="Game over!", anchor="center", fill="red", tag="game_over")

    restart_button = tk.Button(window, text="Restart", fg="red",
                               width=12, height=1,
                               command=lambda: restart_var.set(1))
    restart_button.place(y=-10, relx=0.5, rely=0.6, anchor="s")
    restart_button.wait_variable(restart_var)
    restart_button.destroy()
    canvas.delete("game_over")


def reset_game():
    b.reset_game()
    figure.respawn()


def move():
    if stop:
        return

    if not figure.down():
        b.copy_figure(figure.p, figure.cells, figure.color)
        if not figure.respawn():
            show_game_over(c)
            reset_game()

    window.update()
    s.enter(TIME_VEL, 1, move)
    return


def drop_figure():
    while figure.down():
        window.update()
        tm.sleep(0.1)
    return


def main():
    window.bind('<Key>', on_key)
    window.protocol("WM_DELETE_WINDOW", on_close)

    b.draw()
    figure.respawn()

    s.enter(TIME_VEL, 1, move)
    s.run()


main()
