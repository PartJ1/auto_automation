import tkinter as tk
import pyautogui
from pynput import mouse
from pynput import keyboard
from time import sleep


# init
window = tk.Tk()
window.title('Auto Clicking')
window.geometry('500x500')

wh = pyautogui.size()
print(wh)

recording = False
list_of = []
true_list_of = []
replay = []

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
lb1 = tk.Listbox(my_frame, width=30, height=10)
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
    delay_sec_pure = delay_sec.get()
    if delay_sec_pure != "Delay":
        sleep(int(delay_sec_pure[:-1]))
    for action in replay:
        if action[0] == "key":
            if len(str(action[1])) == 3:
                key = str(action[1])[1]
            else:
                key = str(action[1]).split(".")[1].split(":")[0]
            pyautogui.press(key)
            print(key)

        elif action[0] == "click":
            ignore, x, y, button, up_or = action
            print(x, y, button, up_or)
            if up_or:
                pyautogui.mouseDown(button=str(button).split(".")[1], x=x, y=y)
            else:
                pyautogui.mouseUp(button=str(button).split(".")[1], x=x, y=y)

        elif action[0] == "scroll":
            x, y, dx, dy = action[1:]


def record_fn():
    global recording
    global list_of
    print(recording)

    def on_press(key):
        if recording:
            pass
        else:
            print("RETURNING FALSE")
            return False
        print(["key", key])
        list_of.append(["key", key])

    def on_click(x, y, button, pressed):
        if recording:
            pass
        else:
            return False
        print(["click", x, y, button, pressed])
        list_of.append(["click", x, y, button, pressed])

    def on_scroll(x, y, dx, dy):
        if recording:
            pass
        else:
            return False       
        print(["scroll", x, y, dx, dy])
        list_of.append(["scroll", x, y, dx, dy])

    def on_move(x, y):
        if recording:
            pass
        else:
            return False
        print(f"{x}, {y}")

    print("record started")
    keyboard_listener = keyboard.Listener(on_press=on_press)
    mouse_listener = mouse.Listener(on_click=on_click,
                                    on_scroll=on_scroll,
                                    on_move=on_move)

    if recording is True:
        print("should end")
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
btn_two_frame.pack()
save_btn.pack(side=tk.LEFT, pady=10)
load_btn.pack(side=tk.RIGHT, padx=10)

window.mainloop()