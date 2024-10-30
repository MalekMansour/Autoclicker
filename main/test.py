# Author: Malek Mansour

import tkinter as tk
import threading
import time
import ctypes
import sys

SetCursorPos = ctypes.windll.user32.SetCursorPos
mouse_event = ctypes.windll.user32.mouse_event
MOUSEEVENTF_LEFTDOWN = 0x0002  
MOUSEEVENTF_LEFTUP = 0x0004   
MOUSEEVENTF_RIGHTDOWN = 0x0008  
MOUSEEVENTF_RIGHTUP = 0x0010   

def is_key_pressed(key_code):
    return ctypes.windll.user32.GetAsyncKeyState(key_code) & 0x8000 != 0

class AutoClicker:
    def __init__(self, root):
        self.root = root
        self.root.title("AutoClicker")
        self.root.geometry("350x300")
        
        # Set the application icon
        self.root.iconbitmap("main/assets/logo.ico")  

        self.clicks_per_second = tk.DoubleVar(value=100.0)  # 100 Clicks per second BY DEFAULT
        self.button_choice = tk.StringVar(value="left")
        self.running = False
        self.hotkeys_thread = None
        self.hotkey_start = ord("S")  
        self.hotkey_stop = ord("E")   

        # Clicks per second setting
        tk.Label(root, text="Clicks per Second:").pack(pady=5)
        tk.Entry(root, textvariable=self.clicks_per_second).pack()

        # Button choice setting (Left or Right click)
        tk.Label(root, text="Choose Button to Press:").pack(pady=5)
        button_options = tk.OptionMenu(root, self.button_choice, "left", "right")
        button_options.pack()

        # Start and Stop hotkeys entry fields
        tk.Label(root, text="Start Hotkey:").pack(pady=5)
        self.start_hotkey_entry = tk.Entry(root)
        self.start_hotkey_entry.insert(0, "S")  
        self.start_hotkey_entry.pack()

        tk.Label(root, text="Stop Hotkey:").pack(pady=5)
        self.stop_hotkey_entry = tk.Entry(root)
        self.stop_hotkey_entry.insert(0, "E")  
        self.stop_hotkey_entry.pack()

        # Apply hotkeys button
        tk.Button(root, text="Apply Hotkeys", command=self.apply_hotkeys).pack(pady=5)

        # Start and Stop buttons
        tk.Button(root, text="Start", command=self.start_clicking).pack(pady=5)
        tk.Button(root, text="Stop", command=self.stop_clicking).pack(pady=5)

        # Overlay window for status display
        self.status_window = tk.Toplevel(root)
        self.status_window.overrideredirect(True)
        self.status_window.attributes("-topmost", True)
        self.status_window.geometry("150x30+10+10")
        self.status_window.configure(bg="black")
        
        # Status label with default "Off" setting
        self.status_label = tk.Label(self.status_window, text="Autoclicker: Off", font=("Arial", 12),
                                     bg="black", fg="red")  
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
            self.update_status("Autoclicker: On", "lime") 
            threading.Thread(target=self.click_mouse).start()

    def stop_clicking(self):
        self.running = False
        self.update_status("Autoclicker: Off", "red")  

    def apply_hotkeys(self):
        # Get new hotkeys from the entry fields and update the hotkey codes
        start_key = self.start_hotkey_entry.get().upper()
        stop_key = self.stop_hotkey_entry.get().upper()
        
        if len(start_key) == 1:
            self.hotkey_start = ord(start_key)
            print(f"Start hotkey set to '{start_key}'")
        
        if len(stop_key) == 1:
            self.hotkey_stop = ord(stop_key)
            print(f"Stop hotkey set to '{stop_key}'")

    def monitor_hotkeys(self):
        while True:
            if is_key_pressed(self.hotkey_start):
                self.start_clicking()
            elif is_key_pressed(self.hotkey_stop):
                self.stop_clicking()
            time.sleep(0.1)

    def update_status(self, status_text, color):
        """Updates the status overlay with new text and color."""
        self.status_label.config(text=status_text, fg=color)
        self.status_window.deiconify()

    def emergency_quit(self):
        """Immediately exits the program."""
        self.running = False
        self.update_status("Autoclicker: Off", "red")
        self.root.quit()
        sys.exit()

root = tk.Tk()
app = AutoClicker(root)
root.mainloop()
