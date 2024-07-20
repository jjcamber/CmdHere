import json
import threading
from tkinter import Tk, Label, Entry, Button
import keyboard
import subprocess
from pystray import Icon as icon, MenuItem as item, Menu
from PIL import Image
import threading


# Load initial hotkey from options.json
def load_hotkey():
    with open("options.json", "r") as file:
        return json.load(file)["hotkey"]

hotkey = load_hotkey()

# Function to execute the PowerShell script
def run_powershell_script():
    subprocess.run(["powershell.exe", "-File", "cmd_here.ps1"], shell=True)

# Function to start listening for the hotkey
def start_hotkey_listener():
    keyboard.add_hotkey(hotkey, run_powershell_script)

# GUI for changing the hotkey
def open_gui():
    global hotkey
    keyboard.unhook_all_hotkeys()

    root = Tk()
    root.title("Change Hotkey")

    def save_new_hotkey():
        global hotkey
        hotkey = entry.get()
        with open("options.json", "w") as file:
            json.dump({"hotkey": hotkey}, file)
        keyboard.add_hotkey(hotkey, run_powershell_script)
        root.destroy()

    Label(root, text="Enter new hotkey:").pack()
    entry = Entry(root)
    entry.pack()
    entry.insert(0, hotkey)

    Button(root, text="Save", command=save_new_hotkey).pack()
    Button(root, text="Close", command=root.destroy).pack()

    root.mainloop()

icon_image = Image.open("icon.ico")

def main():
    setup_tray_icon()

# Move threading to the tray icon setup
def setup_tray_icon():
    tray_icon = icon('TestApp', icon_image, menu=Menu(
        item('Open', open_gui),
        item('Exit', lambda: exit_application(tray_icon))
    ))
    # Start the hotkey listener in a thread as the icon runs
    threading.Thread(target=start_hotkey_listener, daemon=True).start()
    tray_icon.run()

def exit_application(tray_icon):
    tray_icon.stop()
    keyboard.unhook_all_hotkeys()

if __name__ == '__main__':
    main()
