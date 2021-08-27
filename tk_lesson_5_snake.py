# lesson 5: snake game:
#   - game over
#   - restart game
#   - scoring hall
#
import sched
import time
import random
import tkinter as tk

window = tk.Tk()
window.title("Snake")

s = sched.scheduler(time.time, time.sleep)

MX = MY = 10
PX = PY = 4

CELLS_X = 30
CELLS_Y = 20
SCORE_HEIGHT = 40
wx = wy = 24

W = wx*CELLS_X + 2*MX + 2*PX
H = wy*CELLS_Y + 2*MY + 3*PY + SCORE_HEIGHT

INI_SNAKE_LEN = 4
x = CELLS_X // 2
y = CELLS_Y // 2
d = 1

stop = False
cells = []
food = []
snake_len = INI_SNAKE_LEN

canvas = tk.Canvas(window, width=W, height=H, bg='white')
canvas.pack()

restart_var = tk.IntVar()


def get_x(cx):
    return MX + PX + cx*wx


def get_y(cy):
    return MY + PY + cy*wy


def draw_board():
    canvas.create_rectangle(MX, MY,
                            get_x(CELLS_X)+PX,
                            get_y(CELLS_Y)+PY, fill="white", outline="black")


def draw_pane():
    canvas.create_rectangle(MX, get_y(CELLS_Y)+MY,
                            get_x(CELLS_X)+PX,
                            get_y(CELLS_Y)+MY+SCORE_HEIGHT,
                            fill="gray")

    yy = get_y(CELLS_Y)+MY+SCORE_HEIGHT // 2
    canvas.create_text(2*MX+PX, yy,
                       text="Score", anchor="w", fill="white")

    canvas.create_text(2*MX+PX+100, yy,
                       text=str(snake_len), anchor="e", fill="white")


def show_game_over():
    canvas.create_rectangle(get_x(CELLS_X // 2 - 6), get_y(CELLS_Y // 2 - 3),
                            get_x(CELLS_X // 2 + 6), get_y(CELLS_Y // 2 + 3),
                            fill="gray")
    xx = get_x(CELLS_X) // 2 + wx // 2
    yy = get_y(CELLS_Y) // 2 - wy
    canvas.create_text(xx, yy, font=("Verdana", 22),
                       text="Game over!", anchor="center", fill="red")

    restart_var.set(0)
    restart_button = tk.Button(window, text="Restart", fg="red",
                               width=12, height=1,
                               command=lambda: restart_var.set(1))
    restart_button.place(relx=0.5, rely=0.5, anchor="c")
    restart_button.wait_variable(restart_var)
    restart_button.destroy()


def add_random_food():
    p = (random.randint(0, CELLS_X - 1), random.randint(0, CELLS_Y - 1))
    while in_snake(p[0], p[1]):
        p = (random.randint(0, CELLS_X - 1), random.randint(0, CELLS_Y - 1))
    food.append(p)


def show_food(xx, yy):
    canvas.create_oval(get_x(xx), get_y(yy), get_x(xx) + wx, get_y(yy) + wy, fill="red")


def draw_food():
    for cx, cy in food:
        show_food(cx, cy)


def draw_head(xx, yy):
    canvas.create_rectangle(get_x(xx), get_y(yy), get_x(xx)+wx, get_y(yy)+wy, fill="green")


def hide_head(xx, yy):
    canvas.create_rectangle(get_x(xx), get_y(yy), get_x(xx)+wx, get_y(yy)+wy, fill="white")


def hide_rect(xx, yy):
    canvas.create_rectangle(get_x(xx), get_y(yy), get_x(xx)+wx, get_y(yy)+wy, fill="white", outline="white")


def draw_snake():
    global cells
    cells = [(x, y)]
    draw_head(x, y)


def in_food(xx, yy):
    for i, p in enumerate(food):
        if p[0] == xx and p[1] == yy:
            return i
    return -1


def in_snake(xx, yy):
    for i, p in enumerate(cells):
        if p[0] == xx and p[1] == yy:
            return True
    return False


def reset_game():
    global cells, food, snake_len
    cells = []
    food = []
    snake_len = INI_SNAKE_LEN

    add_random_food()
    draw_board()
    draw_pane()
    draw_food()
    draw_snake()


def on_time():
    global x, y, cells, food, snake_len, stop
    hide_head(x, y)
    if d == 1:
        y = y - 1 if y-1 >= 0 else y - 1 + CELLS_Y
    elif d == 2:
        y = (y + 1) % CELLS_Y
    elif d == 3:
        x = x - 1 if x-1 >= 0 else x - 1 + CELLS_X
    elif d == 4:
        x = (x + 1) % CELLS_X

    i = in_food(x, y)
    if i >= 0:
        snake_len += 4
        del food[i]
        add_random_food()
        draw_food()
        draw_pane()

    if in_snake(x, y):
        show_game_over()

        # to continue game
        reset_game()
        s.enter(0.2, 1, on_time)
        s.run()
        return

    cells.append((x, y))
    draw_head(x, y)
    if len(cells) > snake_len:
        x0, y0 = cells[0]
        del cells[0]
        hide_rect(x0, y0)
        x0, y0 = cells[0]
        hide_head(x0, y0)

    window.update()
    if not stop:
        s.enter(0.2, 1, on_time)
    return


def onkey(event):
    global stop
    if event.keysym == 'Escape':
        stop = True
        return

    global d
    if event.keysym == 'Up':
        d = 1
    elif event.keysym == 'Down':
        d = 2
    elif event.keysym == 'Left':
        d = 3
    elif event.keysym == 'Right':
        d = 4
    return


def on_closing():
    global stop
    if stop:
        window.quit()
    stop = True
    restart_var.set(1)


def main():
    window.bind('<Key>', onkey)
    window.protocol("WM_DELETE_WINDOW", on_closing)

    for _ in range(5):
        add_random_food()
    draw_board()
    draw_pane()
    draw_food()
    draw_snake()

    s.enter(0.2, 1, on_time)
    s.run()


main()
