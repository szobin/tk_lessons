# - score board
# home task: - levels (show level, add level each 100 points, move figures faster proportional by level)

import tkinter as tk
import sched as sd
import time as tm
import random

BLOCK_COLORS = ['blue2', 'gold2', 'green2', 'cyan2', 'purple2']

BLOCK_1 = [(0, 0), (0, 1), (0, 2), (0, 3)]  # stick
BLOCK_2 = [(0, 0), (1, 0), (2, 0), (1, 1)]  # t-shirt
BLOCK_3 = [(0, 0), (0, 1), (1, 1), (1, 0)]  # rectangle
BLOCK_4 = [(0, 0), (0, 1), (0, 2), (1, 2)]  # G-left
BLOCK_5 = [(0, 0), (0, 1), (0, 2), (-1, 2)]  # G-right
!BLOCK_6 = [(0, 0), (0, 1), (0, 2), (1, 2)]  # S-left
!BLOCK_7 = [(0, 0), (0, 1), (0, 2), (-1, 2)]  # S-right
BLOCK_TYPES = [BLOCK_1, BLOCK_2, BLOCK_3, BLOCK_4, BLOCK_5]

# margins
MX = 10
MY = 10

# padding
PX = 4
PY = 4

# cells
CW = 28
CH = 28

CELLS_X = 12
CELLS_Y = 22

W_PANE = 80
W_CANVAS = CELLS_X*CW + 4*MX + PX + W_PANE
H_CANVAS = CELLS_Y*CH + 2*MY + 2*PY

# velocity
TIME_VEL = 0.4


def get_x(cx):
    return cx*CW + MX + PX


def get_y(cy):
    return cy*CH + MY + PX


def zero_str(v, n):
    sv = str(v)
    return '0'*(n-len(sv)) + sv


def rotate_cells(cells):
    ax, ay = cells[0]
    cells_r = [(ax, ay)]
    for i in range(1, len(cells)):
        c = cells[i]
        bx, by = c[0] - ax, c[1] - ay
        cx, cy = ax - by, ay + bx
        cells_r.append((cx, cy))
    return cells_r


class Board:

    def __init__(self, canvas, nx=CELLS_X, ny=CELLS_Y):
        self.canvas = canvas
        self.nx = nx
        self.ny = ny
        self.cells = []
        self.score = 0
        self.level = 1

    def draw_cell(self, cx, cy, color):
        x = get_x(cx)
        y = get_y(cy)
        self.canvas.create_rectangle(x, y, x+CW, y+CH, fill=color, outline="black")

    def draw_pane(self):
        x = get_x(self.nx) + 2*PX + MX
        y = get_y(self.ny) + PY
        self.canvas.create_rectangle(x, MY,
                                     x + W_PANE,
                                     y, fill="gray")
        self.canvas.create_text(x+MX, MY*3,
                                text="Score", anchor="w", fill="white",
                                font=("Helvetica", 14))

        self.canvas.create_text(x+MX, MY*7,
                                text=zero_str(self.score, 5), anchor="w", fill="gold2",
                                font=("Helvetica", 14))

        self.canvas.create_text(x+MX, MY*11,
                                text="Level", anchor="w", fill="white",
                                font=("Helvetica", 14))

        self.canvas.create_text(x+MX, MY*15,
                                text=zero_str(self.level, 5), anchor="w", fill="gold2",
                                font=("Helvetica", 14))

    def draw_board(self):
        self.canvas.create_rectangle(MX, MY,
                                     get_x(self.nx) + PX,
                                     get_y(self.ny) + PY, fill="white")
        for cx, cy, color in self.cells:
            self.draw_cell(cx, cy, color)

    def draw(self):
        self.draw_board()
        self.draw_pane()

    def copy_figure(self, p, cells, color):
        for cx, cy in cells:
            self.cells.append([cx + p[0], cy + p[1], color])
        self.draw()

    def del_line(self, y):
        self.cells = list(filter(lambda c: c[1] != y, self.cells))

    def shift_uppers(self, y):
        self.cells = list(map(lambda c: c if c[1] > y else (c[0], c[1]+1, c[2]), self.cells))

    def check_full_lines(self):
        lines = {}
        for cx, cy, color in self.cells:
            # if cy in lines:
            #     lines[cy] = lines[cy] + [cx]
            # else:
            #     lines[cy] = [cx]
            lines[cy] = lines[cy] + [cx] if cy in lines else [cx]
                
        for y in lines:
            if len(lines[y]) == CELLS_X:  # line full
                self.del_line(y)
                self.shift_uppers(y)
                return True
        return False

    def reset_game(self):
        self.cells = []

    def in_cells(self, cx, cy):
        for c in self.cells:
            if (c[0] == cx) and (c[1] == cy):
                return True
        return False

    def add_score(self, d_score):
        self.score += d_score

        if self.score > 1000*self.level:
            self.level += 1

        self.draw_pane()

    def get_sleep_time(self):
        return 1/(2+self.level)


class Figure:
    color = None
    cells = None
    p = None

    def __init__(self, canvas, board):
        self.canvas = canvas
        self.board = board
        self.respawn()

    def respawn(self):
        n = random.randint(0, len(BLOCK_TYPES)-1)
        self.color = BLOCK_COLORS[n]
        self.cells = BLOCK_TYPES[n]
        self.p = (random.randint(2, CELLS_X - 4), 0)

    def hide_cell(self, cx, cy):
        # x = get_x(cx + self.p[0])
        # y = get_y(cy + self.p[1])
        # self.canvas.create_rectangle(x, y, x+CW, y+CH, fill="white", outline="white")
        self.canvas.delete("cell{}_{}".format(cx, cy))

    def show_cell(self, cx, cy):
        x = get_x(cx + self.p[0])
        y = get_y(cy + self.p[1])
        self.canvas.create_rectangle(x, y, x+CW, y+CH, fill=self.color, outline="black", tag="cell{}_{}".format(cx, cy))

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


class App:
    def __init__(self):
        self.root = tk.Tk()

        self.root.wm_title("Tetris")
        self.set_window(W_CANVAS, H_CANVAS)

        self.s = sd.scheduler(tm.time, tm.sleep)

        self.canvas = tk.Canvas(self.root, width=W_CANVAS, height=H_CANVAS, bg='white')
        self.canvas.pack()
        self.board = Board(self.canvas)
        self.figure = Figure(self.canvas, self.board)

        self.restart_var = tk.IntVar()
        self.stop = False

    def set_window(self, w, h):
        screen_width = self.root.winfo_screenwidth()
        x = (screen_width // 2) - (w // 2)
        y = 5  # (screen_height // 2) - (h // 2) - 20
        self.root.geometry('%dx%d+%d+%d' % (w, h, x, y))

    def on_key(self, event):
        # to prevent move figure in game-over mode
        if self.stop:
            return

        if event.keysym == 'Escape':
            self.stop = True
            return

        elif event.keysym == 'Left':
            self.figure.shift(-1)
        elif event.keysym == 'Right':
            self.figure.shift(1)
        elif event.keysym == 'Up':
            self.figure.rotate()
        elif event.keysym == 'Down':
            self.drop()

    def on_close(self):
        if self.stop:
            self.root.quit()
        self.stop = True
        self.restart_var.set(1)

    def show_game_over(self):
        self.canvas.create_rectangle(get_x(CELLS_X // 2 - 6), get_y(CELLS_Y // 2 - 3),
                                     get_x(CELLS_X // 2 + 6), get_y(CELLS_Y // 2 + 3),
                                     fill="gray")
        xx = get_x(CELLS_X) // 2 + CW // 2
        yy = get_y(CELLS_Y) // 2 - CH
        self.canvas.create_text(xx, yy, font=("Purisa", 22),
                                text="Game over!", anchor="center", fill="red")

        self.restart_var.set(0)
        restart_button = tk.Button(self.root, text="Restart", fg="red",
                                   width=12, height=1,
                                   command=lambda: self.restart_var.set(1))
        restart_button.place(relx=0.5, rely=0.6, anchor=tk.CENTER)
        restart_button.wait_variable(self.restart_var)
        restart_button.destroy()

    def move(self):

        if self.stop:
            return

        if not self.figure.down():
            self.board.copy_figure(self.figure.p, self.figure.cells, self.figure.color)
            while self.board.check_full_lines():
                self.board.draw()
                self.board.add_score(10)
                self.root.update()
                tm.sleep(0.1)

            self.figure.respawn()
            if not self.figure.check(self.figure.p):
                self.stop = True
                self.show_game_over()

                # to continue game
                self.board.reset_game()
                self.board.draw()
                self.stop = False
            self.board.add_score(1)
            self.figure.show()
        self.root.update()
        self.s.enter(TIME_VEL, 1, self.move)
        return

    def drop(self):
        while self.figure.down():
            self.root.update()
            tm.sleep(0.1)
        return

    def run(self):
        self.board.draw()
        self.figure.show()
        self.root.bind('<Key>', self.on_key)
        self.root.protocol("WM_DELETE_WINDOW", self.on_close)

        self.s.enter(self.board.get_sleep_time(), 1, self.move)
        self.s.run()


def main():
    app = App()
    app.run()


main()
