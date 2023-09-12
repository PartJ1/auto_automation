import tkinter as tk
import csv
from tkinter import filedialog
import pyautogui
from pynput import mouse
from pynput import keyboard
from time import sleep


# init
window = tk.Tk()
window.title('Auto Clicking')
window.geometry('500x500')

wh = pyautogui.size()

recording = False
list_of = []
true_list_of = []
replay = []
stop_key = "key.esc"

# dlt menu
dlt_menu = tk.Menu(window, tearoff=False)

# btn top
btn_one_frame = tk.Frame(window)
record_btn = tk.Button(btn_one_frame, text="Record")
play_btn = tk.Button(btn_one_frame, text="Play")
clear_btn = tk.Button(btn_one_frame, text="Clear")

# delay drop down menu
options = [
    "1s",
    "3s",
    "5s",
    "10s",
    "20s",
    "30s",
]
delay_sec = tk.StringVar()
delay_sec.set("Delay")

delay_btn = tk.OptionMenu(btn_one_frame, delay_sec, options[0], options[1], options[2], options[3], options[4], options[5])

# list of actions
my_frame = tk.Frame(window)
lb1 = tk.Listbox(my_frame, width=35, height=20, selectmode=tk.SINGLE)
scrollbar = tk.Scrollbar(my_frame)
lb1.config(yscrollcommand=scrollbar.set)
scrollbar.config(command=lb1.yview)

# btn bottom
btn_two_frame = tk.Frame(window)
save_btn = tk.Button(btn_two_frame, text="Save")
load_btn = tk.Button(btn_two_frame, text="Load")

# functions
def play_back():
    global delay_sec
    global replay

    bool_replay = True

    delay_sec_pure = delay_sec.get()
    if delay_sec_pure != "Delay":
        sleep(int(delay_sec_pure[:-1]))
    while bool_replay:
        for action in replay:
            if pyautogui.is_pressed('esc'):
                bool_replay = False
                break
            if action[0] == "key":
                if len(str(action[1])) == 3:
                    key = str(action[1])[1]
                else:
                    key = str(action[1]).split(".")[1].split(":")[0]
                pyautogui.press(key)

            elif action[0] == "click":
                ignore, x, y, button, up_or = action
                if up_or:
                    pyautogui.mouseDown(button=str(button).split(".")[1], x=x, y=y)
                else:
                    pyautogui.mouseUp(button=str(button).split(".")[1], x=x, y=y)

            elif action[0] == "scroll":
                x, y, dx, dy = action[1:]
                if dy != 0:
                    pyautogui.scroll(dy)
                else:
                    pyautogui.hscroll(dx)


def record_fn():
    global recording
    global list_of

    def on_press(key):
        if recording:
            pass
        else:
            return False
        list_of.append(["key", key])

    def on_click(x, y, button, pressed):
        if recording:
            pass
        else:
            return False
        list_of.append(["click", x, y, button, pressed])

    def on_scroll(x, y, dx, dy):
        if recording:
            pass
        else:
            return False       
        list_of.append(["scroll", x, y, dx, dy])

    def on_move(x, y):
        if recording:
            pass
        else:
            return False

    keyboard_listener = keyboard.Listener(on_press=on_press)
    mouse_listener = mouse.Listener(on_click=on_click,
                                    on_scroll=on_scroll,
                                    on_move=on_move)

    if recording is True:
        recording = False
        for i in list_of:
            lb1.insert('end', i)
            replay.append(i)
        list_of = []

    else:
        recording = True
        keyboard_listener.start()
        mouse_listener.start()

def clear_fn():
    global lb1
    global list_of
    global replay
    replay = []
    lb1.delete(0, tk.END)

def save_file():
    global replay
    f = filedialog.asksaveasfile(initialfile = 'Untitled.csv',defaultextension=".csv",filetypes=[("Spread Sheets","*.csv")], initialdir="/savefiles")
    try:
        with open(str(f).split("'")[1], "w") as f:
            wr = csv.writer(f)
            wr.writerows(replay)
    except IndexError:
        pass

def load_file():
    global replay
    global lb1
    replay = []
    f = filedialog.askopenfile(defaultextension=".csv",filetypes=[("Spread Sheets","*.csv")], initialdir="/savefiles")
    try:
        with open(str(f).split("'")[1], "r") as f:
            wr = csv.reader(f)
            for row in wr:
                replay.append(row)

        for i in replay:
            lb1.insert('end', i)
    except IndexError:
        pass

def ask_delete(e):
    dlt_menu.tk_popup(e.x, e.y)

def dlt_item():
    for item in lb1.curselection():
        lb1.delete(item)
        replay.pop(item)

# dlt listbox item
dlt_menu.add_command(label="DELETE", command=dlt_item)
lb1.bind('<<ListboxSelect>>', ask_delete)

# btn top
record_btn.config(command=record_fn)
play_btn.config(command=play_back)
clear_btn.config(command=clear_fn)
btn_one_frame.pack()
record_btn.pack(side=tk.LEFT, pady=10)
clear_btn.pack(side=tk.RIGHT, padx=10)
delay_btn.pack(side=tk.RIGHT)
play_btn.pack(side=tk.RIGHT, padx=10)

# list
my_frame.pack()
lb1.pack(side=tk.LEFT, fill=tk.BOTH)
scrollbar.pack(side=tk.RIGHT, fill=tk.BOTH)

# btn buttom
save_btn.config(command=save_file)
load_btn.config(command=load_file)

btn_two_frame.pack()
save_btn.pack(side=tk.LEFT, pady=10)
load_btn.pack(side=tk.RIGHT, padx=10)

window.mainloop()
