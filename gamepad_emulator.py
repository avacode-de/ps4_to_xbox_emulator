import tkinter as tk
import threading
import vgamepad as vg
import inputs

def map_ps4_to_xbox(code):
    """Функция для сопоставления кнопок PS4 с кнопками Xbox"""
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
                button = map_ps4_to_xbox(event.code)
                if button:
                    if event.state: 
                        gamepad.press_button(button)
                        log_text.insert(tk.END, f"Pressed: {event.code}\n")
                    else:  
                        gamepad.release_button(button)
                        log_text.insert(tk.END, f"Released: {event.code}\n")
                    gamepad.update()  

            elif event.ev_type == "Absolute":
                if event.code == "ABS_X": 
                    left_stick_x = event.state
                    gamepad.left_joystick(x_value=left_stick_x, y_value=left_stick_y)
                    log_text.insert(tk.END, f"Left Stick X: {left_stick_x}\n")
                elif event.code == "ABS_Y":  
                    left_stick_y = event.state
                    gamepad.left_joystick(x_value=left_stick_x, y_value=left_stick_y)
                    log_text.insert(tk.END, f"Left Stick Y: {left_stick_y}\n")
                elif event.code == "ABS_RX": 
                    right_stick_x = event.state
                    gamepad.right_joystick(x_value=right_stick_x, y_value=right_stick_y)
                    log_text.insert(tk.END, f"Right Stick X: {right_stick_x}\n")
                elif event.code == "ABS_RY": 
                    right_stick_y = event.state
                    gamepad.right_joystick(x_value=right_stick_x, y_value=right_stick_y)
                    log_text.insert(tk.END, f"Right Stick Y: {right_stick_y}\n")
                elif event.code == "ABS_Z": 
                    gamepad.left_trigger(value=event.state)
                    log_text.insert(tk.END, f"Left Trigger: {event.state}\n")
                elif event.code == "ABS_RZ": 
                    gamepad.right_trigger(value=event.state)
                    log_text.insert(tk.END, f"Right Stick: {event.state}\n")
                gamepad.update()
            log_text.see(tk.END) 

def start_emulator(log_text):
    threading.Thread(target=run_emulator, args=(log_text,), daemon=True).start()

def create_gui():
    root = tk.Tk()
    root.title("PS4 to Xbox Gamepad Emulator")

    log_text = tk.Text(root, height=20, width=50)
    log_text.pack()

    start_button = tk.Button(root, text="Start Emulator", command=lambda: start_emulator(log_text))
    start_button.pack()

    root.mainloop()

if __name__ == "__main__":
    create_gui()
