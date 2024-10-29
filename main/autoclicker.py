# Author: Malek Mansour

import tkinter as tk
import threading
import time
import ctypes
import sys

# Low-level access for mouse events
SetCursorPos = ctypes.windll.user32.SetCursorPos
mouse_event = ctypes.windll.user32.mouse_event
MOUSEEVENTF_LEFTDOWN = 0x0002  
MOUSEEVENTF_LEFTUP = 0x0004   
MOUSEEVENTF_RIGHTDOWN = 0x0008  
MOUSEEVENTF_RIGHTUP = 0x0010   

# Function to get the state of a specific key
def is_key_pressed(key_code):
    return ctypes.windll.user32.GetAsyncKeyState(key_code) & 0x8000 != 0

class AutoClicker:
    def __init__(self, root):
        self.root = root
        self.root.title("AutoClicker")
        self.root.geometry("350x300")
        
        # Variables for click rate, button choice, and click status
        self.clicks_per_second = tk.DoubleVar(value=1.0)
        self.button_choice = tk.StringVar(value="left")
        self.running = False
        self.hotkeys_thread = None
        self.hotkey_start = 0x53  # ASCII code for 'S'
        self.hotkey_stop = 0x45   # ASCII code for 'E'

        # Clicks per second setting
        tk.Label(root, text="Clicks per Second:").pack(pady=5)
        tk.Entry(root, textvariable=self.clicks_per_second).pack()

        # Button choice setting (Left or Right click)
        tk.Label(root, text="Choose Button to Press:").pack(pady=5)
        button_options = tk.OptionMenu(root, self.button_choice, "left", "right")
        button_options.pack()

        # Start and Stop hotkeys
        tk.Label(root, text="Start Hotkey (S):").pack(pady=5)
        tk.Label(root, text="Stop Hotkey (E):").pack(pady=5)

        # Start and Stop buttons
        tk.Button(root, text="Start", command=self.start_clicking).pack(pady=5)
        tk.Button(root, text="Stop", command=self.stop_clicking).pack(pady=5)

        # Overlay window for status display
        self.status_window = tk.Toplevel(root)
        self.status_window.overrideredirect(True)
        self.status_window.attributes("-topmost", True)
        self.status_window.geometry("150x30+10+10")
        self.status_window.configure(bg="black")
        
        self.status_label = tk.Label(self.status_window, text="Autoclicker: Off", font=("Arial", 12),
                                     bg="black", fg="lime")
        self.status_label.pack()
        self.status_window.withdraw()  # Hide initially

        # Start monitoring for hotkeys in a separate thread
        self.hotkeys_thread = threading.Thread(target=self.monitor_hotkeys)
        self.hotkeys_thread.daemon = True
        self.hotkeys_thread.start()

    def click_mouse(self):
        interval = 1 / self.clicks_per_second.get()
        while self.running:
            if interval > 0:
                if self.button_choice.get() == "left":
                    mouse_event(MOUSEEVENTF_LEFTDOWN, 0, 0, 0, 0)
                    mouse_event(MOUSEEVENTF_LEFTUP, 0, 0, 0, 0)
                elif self.button_choice.get() == "right":
                    mouse_event(MOUSEEVENTF_RIGHTDOWN, 0, 0, 0, 0)
                    mouse_event(MOUSEEVENTF_RIGHTUP, 0, 0, 0, 0)
                time.sleep(interval)
            else:
                print("Invalid clicks per second setting.")

    def start_clicking(self):
        if not self.running:
            self.running = True
            self.update_status("Autoclicker: On")
            threading.Thread(target=self.click_mouse).start()

    def stop_clicking(self):
        self.running = False
        self.update_status("Autoclicker: Off")

    def monitor_hotkeys(self):
        while True:
            if is_key_pressed(self.hotkey_start):
                self.start_clicking()
            elif is_key_pressed(self.hotkey_stop):
                self.stop_clicking()
            time.sleep(0.1)

    def update_status(self, status_text):
        """Updates the status overlay with new text."""
        self.status_label.config(text=status_text)
        if status_text == "Autoclicker: On":
            self.status_window.deiconify()
        else:
            self.status_window.withdraw()

    def emergency_quit(self):
        """Immediately exits the program."""
        self.running = False
        self.update_status("Autoclicker: Off")
        self.root.quit()
        sys.exit()

# Run the Tkinter GUI
root = tk.Tk()
app = AutoClicker(root)
root.mainloop()
