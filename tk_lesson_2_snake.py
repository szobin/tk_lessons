# lesson 2: snake game:
#   - board
#   - snake head and body
#   - how to use arrow keys
import tkinter as tk

W = 700
H = 500
CW = CH = 20

window = tk.Tk()
window.title("Snake")

x = y = W // 2

canvas = tk.Canvas(window, width=W, height=H, bg='white')
canvas.pack()


def draw_head():
    canvas.create_rectangle(x, y, x + CW, y + CH, fill="green", tag="head")


def hide_head():
    canvas.delete("head")


# def on_key(event):
#     global x, y
#     hide_head()
#
#     if event.keysym == 'Up':
#         y = y - CH if y-CH > 0 else y - 2*CH + H
#     elif event.keysym == 'Down':
#         y = (y + CH) % (H - CH)
#     elif event.keysym == 'Left':
#         x = x - CW if x - CW > 0 else x - 2*CW + W
#     elif event.keysym == 'Right':
#         x = (x + CW) % (W - CH)
#
#     draw_head()


def key_up(xx, yy):
    return xx, yy - CH if yy-CH > 0 else yy - 2*CH + H


def on_key(event):
    global x, y
    case = {'Up': key_up,  # lambda xx, yy: (xx, yy - CH if yy-CH > 0 else yy - 2*CH + H),
            'Down': lambda xx, yy: (xx, (yy + CH) % (H - CH)),
            'Left': lambda xx, yy: (xx - CW if xx - CW > 0 else xx - 2*CW + W, yy),
            'Right': lambda xx, yy: ((xx + CW) % (W - CH), yy)}
    if event.keysym in case:
        hide_head()
        x, y = case[event.keysym](x, y)
        draw_head()


def main():
    window.bind('<Key>', on_key)

    draw_head()
    window.mainloop()


main()
