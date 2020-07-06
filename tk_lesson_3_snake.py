# lesson 3: snake game:
#   - snake moving
#   - change moving direction by keys

import sched
import time
import tkinter as tk

window = tk.Tk()
window.title("Snake")

s = sched.scheduler(time.time, time.sleep)

BOARD_X = BOARD_Y = 5
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

canvas = tk.Canvas(window, width=CELLS_X*wx+2*BOARD_X, height=CELLS_Y*wy+2*BOARD_Y+SCORE_HEIGHT, bg='white')
canvas.pack()


def draw_board():
    canvas.create_rectangle(BOARD_X, BOARD_Y,
                            BOARD_X + CELLS_X*wx,
                            BOARD_Y + CELLS_X*wy, fill="white")


def draw_head(xx, yy):
    canvas.create_rectangle(xx, yy, xx + wx, yy + wy, fill="green")


def hide_head(xx, yy):
    canvas.create_rectangle(xx, yy, xx + wx, yy + wy, fill="white")


def hide_rect(xx, yy):
    canvas.create_rectangle(xx, yy, xx + wx, yy + wy, fill="white", outline="white")


def draw_snake():
    global snake
    snake = [(x, y)]
    draw_head(x, y)


def on_time():
    global x, y, snake
    hide_head(x, y)
    if d == 1:
        y = y - wy if y-wy > 0 else y - 2*wy + CELLS_Y*wy
    elif d == 2:
        y = (y + wy) % (CELLS_Y*wy - wy)
    elif d == 3:
        x = x - wx if x - wx > 0 else x - 2 * wx + CELLS_X*wx
    elif d == 4:
        x = (x + wx) % (CELLS_X*wx - wx)

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
    stop = True


def main():
    draw_snake()
    window.bind('<Key>', onkey)
    window.protocol("WM_DELETE_WINDOW", on_closing)

    s.enter(0.2, 1, on_time)
    s.run()


main()
