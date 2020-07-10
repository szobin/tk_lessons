# lesson #11
# tetris #5
# score board, score
# home task: - levels (show level, add level each 100 points, move figures faster proportional by level)

import tkinter as tk
import sched as sd
import time as tm
import random

BLOCK_1 = [(0, 0), (0, 1), (0, 2), (0, 3)]  # stick
BLOCK_2 = [(0, 0), (1, 0), (2, 0), (1, 1)]  # t-shirt
BLOCK_3 = [(0, 0), (0, 1), (1, 1), (1, 0)]  # cube
BLOCK_4 = [(0, 0), (0, 1), (0, 2), (1, 2)]  # G-left
BLOCK_5 = [(0, 0), (0, 1), (0, 2), (-1, 2)]  # G-right
BLOCK_6 = [(0, 0), (0, 1), (0, 2), (1, 2)]  # S-left
BLOCK_7 = [(0, 0), (0, 1), (0, 2), (-1, 2)]  # S-right
BLOCK_TYPES = [(BLOCK_1, 'blue2'), (BLOCK_2, 'gold2'), (BLOCK_3, 'green2'),
               (BLOCK_4, 'cyan2'), (BLOCK_5, 'cyan2'),
               (BLOCK_6, 'purple2'), (BLOCK_7, 'purple2')]


# margins
MX = 10
MY = 10

# padding
PX = 4
PY = 4

# cells
CW = 28
CH = 28

N_COLS = 12
N_ROWS = 22

W_PANE = 80
W_CANVAS = N_COLS*CW + 4*MX + PX + W_PANE
H_CANVAS = N_ROWS*CH + 2*MY + 2*PY


def get_x(cx):
    return cx*CW + MX + PX


def get_y(cy):
    return cy*CH + MY + PX


def zero_str(v, n):
    sv = str(v)
    return '0'*(n-len(sv)) + sv


def rotate_cells(cells):
    ax, ay = cells[1]
    cells_new = []
    for cx, cy in cells:
        dx, dy = cx - ax, cy - ay
        bx, by = ax - dy, ay + dx
        cells_new.append((bx, by))
    return cells_new


class Board:
    cells = None
    score = None
    level = None

    def __init__(self, canvas):
        self.canvas = canvas
        self.reset()

    def reset(self):
        self.cells = []
        self.score = 0
        self.level = 1

    def get_interval(self):
        return 0.04 + 1 / (2+self.level)

    def draw_cell(self, cx, cy, color):
        x = get_x(cx)
        y = get_y(cy)
        self.canvas.create_rectangle(x, y, x+CW, y+CH, fill=color, outline="black", tag="cells")

    def draw_pane(self):
        self.canvas.delete("pane")
        x = get_x(N_COLS) + 2*PX + MX
        y = get_y(N_ROWS) + PY
        self.canvas.create_rectangle(x, MY,
                                     x + W_PANE,
                                     y, fill="gray", tag="pane")
        self.canvas.create_text(x+MX, MY*3,
                                text="Score", anchor="w", fill="white",
                                font=("Helvetica", 14), tag="pane")

        self.canvas.create_text(x+MX, MY*7,
                                text=zero_str(self.score, 5), anchor="w", fill="gold2",
                                font=("Helvetica", 14), tag="pane")

        self.canvas.create_text(x+MX, MY*11,
                                text="Level", anchor="w", fill="white",
                                font=("Helvetica", 14), tag="pane")

        self.canvas.create_text(x+MX, MY*15,
                                text=zero_str(self.level, 5), anchor="w", fill="gold2",
                                font=("Helvetica", 14), tag="pane")

    def draw_board(self):
        self.canvas.create_rectangle(MX, MY,
                                     get_x(N_COLS) + PX,
                                     get_y(N_ROWS) + PY, fill="white", tag="board")

    def show_cells(self):
        for cx, cy, color in self.cells:
            self.draw_cell(cx, cy, color)

    def draw(self):
        self.draw_board()
        self.show_cells()
        self.draw_pane()

    def hide_cells(self):
        self.canvas.delete("cells")

    def copy_figure(self, p, cells, color):
        px, py = p
        for cx, cy in\
                cells:
            self.cells.append((cx + px, cy + py, color))
            self.draw_cell(cx + p[0], cy + p[1], color)

    def del_line(self, cy):
        self.cells = list(filter(lambda c: c[1] != cy, self.cells))

    def shift_uppers(self, cy):
        self.cells = list(map(lambda c: c if c[1] > cy else (c[0], c[1]+1, c[2]), self.cells))

    def check_full_line(self):
        lines = {}
        for cx, cy, color in self.cells:
            # if cy in lines:
            #     lines[cy] = lines[cy] + [cx]
            # else:
            #     lines[cy] = [cx]
            lines[cy] = lines[cy] + [cx] if cy in lines else [cx]
                
        for cy in lines:
            if len(lines[cy]) == N_COLS:  # line full
                return cy
        return -1

    def in_cells(self, cx, cy):
        for c in self.cells:
            if (c[0] == cx) and (c[1] == cy):
                return True
        return False

    def process_line(self, cy):
        self.hide_cells()
        self.del_line(cy)
        self.shift_uppers(cy)
        self.show_cells()

    def add_score(self, d_score):
        self.score += d_score

        if self.score > 100*self.level:
            self.level += 1

        self.draw_pane()


class Figure:
    color = None
    cells = None
    p = None

    def __init__(self, canvas, board):
        self.canvas = canvas
        self.board = board
        self.cells, self.color = random.choice(BLOCK_TYPES)
        self.p = (random.randint(2, N_COLS - 4), 0)

    def respawn(self):
        self.cells, self.color = random.choice(BLOCK_TYPES)
        self.p = (random.randint(2, N_COLS - 4), 0)

    def show_cell(self, cx, cy):
        x = get_x(cx + self.p[0])
        y = get_y(cy + self.p[1])
        self.canvas.create_rectangle(x, y, x+CW, y+CH, fill=self.color, outline="black", tag="figure")

    def hide(self):
        self.canvas.delete("figure")

    def show(self):
        for cx, cy in self.cells:
            self.show_cell(cx, cy)

    def check(self, p, cells=None):
        check_cells = cells if cells is not None else self.cells
        for x, y in check_cells:
            xx, yy = x + p[0], y+p[1]
            if (yy < 0) or (yy >= N_ROWS):
                return False
            if (xx < 0) or (xx >= N_COLS):
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

        self.root.bind('<Key>', self.on_key)
        self.root.protocol("WM_DELETE_WINDOW", self.on_close)

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

    def game_over(self):
        x = W_CANVAS / 2
        y = H_CANVAS / 2
        self.canvas.create_rectangle(x - 6*CW, y - 3*CH,
                                     x + 6*CW, y + 3*CH,
                                     fill="red", tag="game")

        self.canvas.create_text(x, y-CH, font=("Purisa", 22),
                                text="Game over!", anchor="center",
                                fill="black", tag="game")

        self.restart_var.set(0)
        restart_button = tk.Button(self.root, text="Restart", fg="red",
                                   width=12, height=1,
                                   command=lambda: self.restart_var.set(1))
        restart_button.place(x=x, y=y + CH + MX, anchor=tk.CENTER)
        restart_button.wait_variable(self.restart_var)
        restart_button.destroy()
        self.canvas.delete("game")

    def on_time(self):

        if self.stop:
            return

        if not self.figure.down():
            self.board.copy_figure(self.figure.p, self.figure.cells, self.figure.color)

            cy = self.board.check_full_line()
            while cy >= 0:
                self.board.process_line(cy)

                self.board.add_score(10)
                self.root.update()
                tm.sleep(0.1)
                cy = self.board.check_full_line()

            self.figure.respawn()
            if not self.figure.check(self.figure.p):
                self.game_over()

                # to continue game
                self.board.reset()
                self.board.draw()
            self.board.add_score(1)
            self.figure.show()
        self.root.update()
        self.s.enter(self.board.get_interval(), 1, self.on_time)
        return

    def drop(self):
        while self.figure.down():
            self.root.update()
            tm.sleep(0.1)
        return

    def run(self):
        self.board.draw()
        self.figure.show()

        self.s.enter(self.board.get_interval(), 1, self.on_time)
        self.s.run()
        # self.root.mainloop()


def main():
    app = App()
    app.run()


main()
