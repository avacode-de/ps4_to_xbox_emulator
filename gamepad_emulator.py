import json
import os
import time
import tkinter as tk
import threading
import vgamepad as vg
import inputs

macros = {}
macros_enabled = True
log_file = "gamepad_log.txt"

def save_macros_to_file(file_path="macros.json"):
    with open(file_path, "w") as file:
        json.dump(macros, file, indent=4)
    print(f"Macros saved to {file_path}")

def load_macros_from_file(file_path="macros.json"):
    global macros
    try:
        with open(file_path, "r") as file:
            macros = json.load(file)
        print(f"Macros loaded from {file_path}")
    except FileNotFoundError:
        print("No macros file found, using default macros.")
        macros = {}  # default empty macros

def switch_profile(profile_name):
    profile_path = f"{profile_name}.json"
    load_macros_from_file(profile_path)
    print(f"Switched to profile: {profile_name}")

def log_action(action):
    with open(log_file, "a") as log:
        log.write(f"{time.strftime('%Y-%m-%d %H:%M:%S')} - {action}\n")

def toggle_macros():
    global macros_enabled
    macros_enabled = not macros_enabled
    status = "enabled" if macros_enabled else "disabled"
    print(f"Macros {status}")
    log_action(f"Macros {status}")

def map_ps4_to_xbox(code):
    mapping = {
        "BTN_SOUTH": vg.XUSB_BUTTON.XUSB_GAMEPAD_A,
        "BTN_EAST": vg.XUSB_BUTTON.XUSB_GAMEPAD_B,
        "BTN_NORTH": vg.XUSB_BUTTON.XUSB_GAMEPAD_Y,
        "BTN_WEST": vg.XUSB_BUTTON.XUSB_GAMEPAD_X,
        "BTN_TL": vg.XUSB_BUTTON.XUSB_GAMEPAD_LEFT_SHOULDER,
        "BTN_TR": vg.XUSB_BUTTON.XUSB_GAMEPAD_RIGHT_SHOULDER,
        "BTN_SELECT": vg.XUSB_BUTTON.XUSB_GAMEPAD_BACK,
        "BTN_START": vg.XUSB_BUTTON.XUSB_GAMEPAD_START,
        "BTN_THUMBL": vg.XUSB_BUTTON.XUSB_GAMEPAD_LEFT_THUMB,
        "BTN_THUMBR": vg.XUSB_BUTTON.XUSB_GAMEPAD_RIGHT_THUMB,
        "BTN_DPAD_LEFT": vg.XUSB_BUTTON.XUSB_GAMEPAD_DPAD_LEFT,
        "BTN_DPAD_RIGHT": vg.XUSB_BUTTON.XUSB_GAMEPAD_DPAD_RIGHT,
        "BTN_DPAD_DOWN": vg.XUSB_BUTTON.XUSB_GAMEPAD_DPAD_DOWN,
        "BTN_DPAD_UP": vg.XUSB_BUTTON.XUSB_GAMEPAD_DPAD_UP,
    }
    return mapping.get(code, None)

def run_emulator(log_text):
    gamepad = vg.VX360Gamepad()

    if not inputs.devices.gamepads:
        log_text.insert(tk.END, "No gamepads detected.\n")
        return

    left_stick_x = 0
    left_stick_y = 0
    right_stick_x = 0
    right_stick_y = 0

    while True:
        events = inputs.get_gamepad()

        for event in events:
            if event.ev_type == "Key":
                if macros_enabled and event.code in macros and event.state:
                    log_text.insert(tk.END, f"Executing macro for: {event.code}\n")
                    execute_macro(gamepad, macros[event.code], log_text) 
                else:
                    button = map_ps4_to_xbox(event.code)
                    if button:
                        if event.state:
                            gamepad.press_button(button)
                            log_text.insert(tk.END, f"Pressed: {event.code}\n")
                            log_action(f"Pressed: {event.code}")
                        else:
                            gamepad.release_button(button)
                            log_text.insert(tk.END, f"Released: {event.code}\n")
                            log_action(f"Released: {event.code}")
                        gamepad.update()

            elif event.ev_type == "Absolute":
                if event.code == "ABS_X":
                    left_stick_x = event.state
                    gamepad.left_joystick(x_value=left_stick_x, y_value=left_stick_y)
                    log_text.insert(tk.END, f"Left Stick X: {left_stick_x}\n")
                    log_action(f"Left Stick X: {left_stick_x}")
                elif event.code == "ABS_Y":
                    left_stick_y = event.state
                    gamepad.left_joystick(x_value=left_stick_x, y_value=left_stick_y)
                    log_text.insert(tk.END, f"Left Stick Y: {left_stick_y}\n")
                    log_action(f"Left Stick Y: {left_stick_y}")
                elif event.code == "ABS_RX":
                    right_stick_x = event.state
                    gamepad.right_joystick(x_value=right_stick_x, y_value=right_stick_y)
                    log_text.insert(tk.END, f"Right Stick X: {right_stick_x}\n")
                    log_action(f"Right Stick X: {right_stick_x}")
                elif event.code == "ABS_RY":
                    right_stick_y = event.state
                    gamepad.right_joystick(x_value=right_stick_x, y_value=right_stick_y)
                    log_text.insert(tk.END, f"Right Stick Y: {right_stick_y}\n")
                    log_action(f"Right Stick Y: {right_stick_y}")
                elif event.code == "ABS_Z":
                    gamepad.left_trigger(value=event.state)
                    log_text.insert(tk.END, f"Left Trigger: {event.state}\n")
                    log_action(f"Left Trigger: {event.state}")
                elif event.code == "ABS_RZ":
                    gamepad.right_trigger(value=event.state)
                    log_text.insert(tk.END, f"Right Trigger: {event.state}\n")
                    log_action(f"Right Trigger: {event.state}")
                gamepad.update()
            log_text.see(tk.END)

def execute_macro(gamepad, macro, log_text):
    gamepad = vg.VX360Gamepad()
    for action in macro:
        button = getattr(vg.XUSB_BUTTON, action[0])
        duration = action[1]
        gamepad.press_button(button)
        log_text.insert(tk.END, f"Macro action: Pressed {action[0]} for {duration} seconds\n")
        time.sleep(duration)
        gamepad.update()
        gamepad.release_button(button)
        log_text.insert(tk.END, f"Macro action: Released {action[0]}\n")
        gamepad.update()

def start_emulator(log_text):
    threading.Thread(target=run_emulator, args=(log_text,), daemon=True).start()

def add_or_update_macro(button, actions):
    global macros
    macros[button] = actions
    save_macros_to_file()
    print(f"Macro for {button} has been updated")

def create_gui():
    root = tk.Tk()
    root.title("PS4 to Xbox Gamepad Emulator")

    log_text = tk.Text(root, height=20, width=50)
    log_text.pack()

    start_button = tk.Button(root, text="Start Emulator", command=lambda: start_emulator(log_text))
    start_button.pack()

    toggle_button = tk.Button(root, text="Toggle Macros", command=toggle_macros)
    toggle_button.pack()

    save_button = tk.Button(root, text="Save Macros", command=save_macros_to_file)
    save_button.pack()

    load_button = tk.Button(root, text="Load Macros", command=load_macros_from_file)
    load_button.pack()

    tk.Label(root, text="Button:").pack()
    button_entry = tk.Entry(root)
    button_entry.pack()

    tk.Label(root, text="Actions (format: button1,duration1;button2,duration2):").pack()
    actions_entry = tk.Entry(root)
    actions_entry.pack()

    def on_add_macro():
        button = button_entry.get()
        actions_input = actions_entry.get()
        actions = [action.split(',') for action in actions_input.split(';')]
        actions = [[action[0], float(action[1])] for action in actions]
        add_or_update_macro(button, actions)
    
    add_macro_button = tk.Button(root, text="Add/Update macro", command=on_add_macro)
    add_macro_button.pack()

    profile_button = tk.Button(root, text="Switch Profile", command=lambda: switch_profile("default"))
    profile_button.pack()

    root.mainloop()

if __name__ == "__main__":
    load_macros_from_file()
    create_gui()
