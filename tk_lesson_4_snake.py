# lesson 4: snake game:
#  - eating food
#  - growing
#  - score pane

import sched
import time
import random
import tkinter as tk

window = tk.Tk()
window.title("Snake")
s = sched.scheduler(time.time, time.sleep)

BOARD_X = BOARD_Y = 10
MARGIN_X = MARGIN_Y = 3
CELLS_X = 30
CELLS_Y = 20
SCORE_HEIGHT = 40
wx = wy = 20

SNAKE_LEN = 4
x = CELLS_X // 2
y = CELLS_Y // 2
d = 1
stop = False
snake = []
food = []

canvas = tk.Canvas(window, width=CELLS_X*wx+2*BOARD_X, height=CELLS_Y*wy+2*BOARD_Y+SCORE_HEIGHT, bg='white')
canvas.pack()


def get_x(xx):
    return BOARD_X + xx*wx


def get_y(yy):
    return BOARD_Y + yy*wy


def draw_board():
    canvas.create_rectangle(BOARD_X-MARGIN_X, BOARD_Y-MARGIN_Y,
                            get_x(CELLS_X)+MARGIN_X,
                            get_y(CELLS_Y)+MARGIN_Y, fill="white")


def draw_pane():
    canvas.create_rectangle(BOARD_X-MARGIN_X, get_y(CELLS_Y)+3*MARGIN_Y,
                            get_x(CELLS_X)+MARGIN_X, get_y(CELLS_Y)+2*MARGIN_Y+SCORE_HEIGHT,
                            fill="gray")
    yy = get_y(CELLS_Y)+2*MARGIN_Y+SCORE_HEIGHT // 2
    canvas.create_text(BOARD_X+MARGIN_X, yy,
                       text="Score", anchor="w", fill="white")

    canvas.create_text(BOARD_X+MARGIN_X+100, yy,
                       text=str(SNAKE_LEN), anchor="e", fill="white")


def add_random_food():
    p = (random.randint(0, CELLS_X - 1), random.randint(0, CELLS_Y - 1))
    while in_snake(p[0], p[1]):
        p = (random.randint(0, CELLS_X - 1), random.randint(0, CELLS_Y - 1))
    food.append(p)


def show_food(xx, yy):
    canvas.create_oval(get_x(xx), get_y(yy), get_x(xx) + wx, get_y(yy) + wy, fill="red")


def draw_food():
    for p in food:
        show_food(p[0], p[1])


def draw_head(xx, yy):
    canvas.create_rectangle(get_x(xx), get_y(yy), get_x(xx)+wx, get_y(yy)+wy, fill="green")


def hide_head(xx, yy):
    canvas.create_rectangle(get_x(xx), get_y(yy), get_x(xx)+wx, get_y(yy)+wy, fill="white")


def hide_rect(xx, yy):
    canvas.create_rectangle(get_x(xx), get_y(yy), get_x(xx)+wx, get_y(yy)+wy, fill="white", outline="white")


def draw_snake():
    global snake
    snake = [(x, y)]
    draw_head(x, y)


def in_food(xx, yy):
    for i, p in enumerate(food):
        if p[0] == xx and p[1] == yy:
            return i
    return -1


def in_snake(xx, yy):
    for i, p in enumerate(snake):
        if p[0] == xx and p[1] == yy:
            return True
    return False


def move():
    global x, y, snake, food, SNAKE_LEN, stop
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
        SNAKE_LEN += 4
        del food[i]
        add_random_food()
        draw_food()
        draw_pane()

    snake.append((x, y))
    draw_head(x, y)
    if len(snake) > SNAKE_LEN:
        x0, y0 = snake[0]
        del snake[0]
        hide_rect(x0, y0)
        x0, y0 = snake[0]
        hide_head(x0, y0)

    window.update()
    if not stop:
        s.enter(0.2, 1, move)
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


def main():
    window.bind('<Key>', onkey)
    window.protocol("WM_DELETE_WINDOW", on_closing)

    add_random_food()
    draw_board()
    draw_pane()
    draw_food()
    draw_snake()

    s.enter(0.2, 1, move)
    s.run()


main()
