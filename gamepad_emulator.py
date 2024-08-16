import tkinter as tk
import vgamepad as vg
import threading
import inputs

def main_ps4_to_xbox(button):
    mapping = {
        "BTN_SOUTH": vg.XUSB_BUTTON.XUSB_GAMEPAD_A,
        "BTN_EAST": vg.XUSB_BUTTON.XUSB_GAMEPAD_B,
        "BTN_NORTH": vg.XUSB_BUTTON.XUSB_GAMEPAD_Y,
        "BTN_WEST": vg.XUSB_BUTTON.XUSB_GAMEPAD_X,
        "BTN_TL": vg.XUSB_BUTTON.XUSB_GAMEPAD_LEFT_SHOULDER,
        "BTN_TR": vg.XUSB_BUTTON.XUSB_GAMEPAD_RIGHT_SHOULDER,
        "BTN_SELECT": vg.XUSB_BUTTON.XUSB_GAMEPAD_BACK,
        "BTN_START": vg.XUSB_BUTTON.XUSB_GAMEPAD_START,
        "BTN_THUML": vg.XUSB_BUTTON.XUSB_GAMEPAD_LEFT_THUMB,
        "BTN_THUMR": vg.XUSB_BUTTON.XUSB_GAMEPAD_RIGHT_THUMB
    }

def run_emu(log_text):
    gamepad = vg.VDS4Gamepad()

    if not inputs.devices.gamepads:
        log_text.insert(tk.END, "No gamepads detected.\n")
        return
    
    left_stick_y = 0
    left_stick_x = 0
    right_stick_y = 0
    right_stick_x = 0

    ps4_controller = inputs.devices.gamepads[0]
    print(inputs.devices.gamepads)

    while True:
        events = inputs.get_gamepad()

        for event in events:
            if event.ev_type == "Key":
                button = main_ps4_to_xbox(event.code)
                if button:
                    if event.state:
                        gamepad.press_button(button)
                        log_text.insert(tk.END, f"Pressed: {event.code}\n")
                    else:
                        gamepad.release_button(button)
                        log_text.insert(tk.END, f"Released: {event.code}\n")
                    gamepad.update()
        
            elif event.ev_type == "Absolute":
                if event.code == "ABS_X":  # Левый стик, ось X
                    left_stick_x = event.state
                    gamepad.left_joystick(x_value=left_stick_x, y_value=left_stick_y)
                elif event.code == "ABS_Y":  # Левый стик, ось Y
                    left_stick_y = event.state
                    gamepad.left_joystick(x_value=left_stick_x, y_value=left_stick_y)
                elif event.code == "ABS_RX":  # Правый стик, ось X
                    right_stick_x = event.state
                    gamepad.right_joystick(x_value=right_stick_x, y_value=right_stick_y)
                elif event.code == "ABS_RY":  # Правый стик, ось Y
                    right_stick_y = event.state
                    gamepad.right_joystick(x_value=right_stick_x, y_value=right_stick_y)
                elif event.code == "ABS_Z":  # Левый триггер
                    gamepad.left_trigger(value=event.state)
                elif event.code == "ABS_RZ":  # Правый триггер
                    gamepad.right_trigger(value=event.state)
                gamepad.update()
            log_text.see(tk.END)

def start_emulator(log_text):
    threading.Thread(target=run_emu, args=(log_text,), daemon=True).start()

def create_gui():
    root = tk.Tk()
    root.title("PS4 to XBOX emulator")

    log_text = tk.Text(root, height= 20, width= 50)
    log_text.pack()

    start_button = tk.Button(root, text = "Start emulator", command=lambda: start_emulator(log_text))
    start_button.pack()

    root.mainloop()

if __name__ == "__main__":
    create_gui()