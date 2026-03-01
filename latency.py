import tkinter as tk
from pynput import mouse
import time
import ctypes

root = tk.Tk()
root.overrideredirect(True)
root.attributes("-topmost", True)

# transparent background
root.config(bg='magenta')
root.wm_attributes("-transparentcolor", "magenta")

# click-through
hwnd = ctypes.windll.user32.GetParent(root.winfo_id())
GWL_EXSTYLE = -20
WS_EX_LAYERED = 0x80000
WS_EX_TRANSPARENT = 0x20
style = ctypes.windll.user32.GetWindowLongW(hwnd, GWL_EXSTYLE)
ctypes.windll.user32.SetWindowLongW(hwnd, GWL_EXSTYLE, style | WS_EX_LAYERED | WS_EX_TRANSPARENT)

FONT = ("Arial", 16, "bold")

# outline
labels = []
offsets = [(-1,-1),(0,-1),(1,-1),(-1,0),(1,0),(-1,1),(0,1),(1,1)]
for dx, dy in offsets:
    lbl = tk.Label(root, font=FONT, fg="black", bg="magenta")
    lbl.place(x=dx, y=dy)
    labels.append(lbl)

main = tk.Label(root, font=FONT, fg="white", bg="magenta")
main.place(x=0, y=0)

press_time = 0
latest = 0

def update_text():
    text = f"Latency: {latest:.2f} ms"
    main.config(text=text)
    for lbl in labels:
        lbl.config(text=text)
    root.geometry("+10+10")

def on_click(x, y, button, pressed):
    global press_time, latest
    if pressed:
        press_time = time.perf_counter()
    else:
        latest = (time.perf_counter() - press_time) * 1000
        update_text()

listener = mouse.Listener(on_click=on_click)
listener.start()

def keep_on_top():
    root.attributes("-topmost", True)
    root.after(500, keep_on_top)

keep_on_top()
root.mainloop()