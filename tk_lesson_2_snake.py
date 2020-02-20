# lesson 2: snake game:
#   - board
#   - snake head and body
#   - how to use arrows
import tkinter as tk

window = tk.Tk()

WIDTH = HEIGHT = 500
x = y = WIDTH // 2
wx = wy = 20

canvas = tk.Canvas(window, width=WIDTH, height=HEIGHT, bg='white')
canvas.pack()


def draw_rect():
    canvas.create_rectangle(x, y, x + wx, y + wy, fill="green")


def hide_rect():
    canvas.create_rectangle(x, y, x + wx, y + wy, fill="white")


def move(event):
    if event.keysym == 'Escape':
        window.quit()
        return

    global x, y
    hide_rect()
    if event.keysym == 'Up':
        y = y - wy if y-wy > 0 else y - 2*wy + HEIGHT
    elif event.keysym == 'Down':
        y = (y + wy) % (HEIGHT - wy)
    elif event.keysym == 'Left':
        x = x - wx if x - wx > 0 else x - 2*wx + WIDTH
    elif event.keysym == 'Right':
        x = (x + wx) % (WIDTH - wx)
    draw_rect()


def main():
    draw_rect()
    window.bind('<Key>', move)
    window.mainloop()


main()
