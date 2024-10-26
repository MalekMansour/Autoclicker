# Autoclicker
# Author: Malek Mansour
import tkinter as tk
import threading
import time
import ctypes

# Set up low-level access for mouse events
SetCursorPos = ctypes.windll.user32.SetCursorPos
mouse_event = ctypes.windll.user32.mouse_event
MOUSEEVENTF_LEFTDOWN = 0x0002  # Left button down
MOUSEEVENTF_LEFTUP = 0x0004    # Left button up

class AutoClicker:
    def __init__(self, root):
        self.root = root
        self.root.title("AutoClicker")
        self.root.geometry("350x200")
        
        # Variables for click interval and click status
        self.interval = tk.DoubleVar(value=1.0)
        self.running = False

        # Interval setting
        tk.Label(root, text="Click Interval (seconds):").pack(pady=5)
        tk.Entry(root, textvariable=self.interval).pack()

        # Hotkey settings for Start and Stop (keys as strings)
        self.start_hotkey = tk.StringVar(value="s")  # Default start hotkey
        self.stop_hotkey = tk.StringVar(value="e")   # Default stop hotkey
        tk.Label(root, text="Start Hotkey:").pack(pady=5)
        tk.Entry(root, textvariable=self.start_hotkey).pack()
        tk.Label(root, text="Stop Hotkey:").pack(pady=5)
        tk.Entry(root, textvariable=self.stop_hotkey).pack()

        # Start and Stop buttons
        tk.Button(root, text="Start", command=self.start_clicking).pack(pady=5)
        tk.Button(root, text="Stop", command=self.stop_clicking).pack(pady=5)
        
        # Bind hotkey checks
        root.bind(f"<KeyPress-{self.start_hotkey.get()}>", lambda e: self.start_clicking())
        root.bind(f"<KeyPress-{self.stop_hotkey.get()}>", lambda e: self.stop_clicking())
        
        # Button to apply new hotkeys
        tk.Button(root, text="Apply Hotkeys", command=self.apply_hotkeys).pack(pady=10)

    def click_mouse(self):
        while self.running:
            mouse_event(MOUSEEVENTF_LEFTDOWN, 0, 0, 0, 0)  # Press mouse down
            mouse_event(MOUSEEVENTF_LEFTUP, 0, 0, 0, 0)    # Release mouse
            time.sleep(self.interval.get())  # Wait for the specified interval

    def start_clicking(self):
        if not self.running:
            self.running = True
            threading.Thread(target=self.click_mouse).start()

    def stop_clicking(self):
        self.running = False

    def apply_hotkeys(self):
        # Rebind hotkeys based on user input
        self.root.bind(f"<KeyPress-{self.start_hotkey.get()}>", lambda e: self.start_clicking())
        self.root.bind(f"<KeyPress-{self.stop_hotkey.get()}>", lambda e: self.stop_clicking())
        print(f"Start hotkey set to '{self.start_hotkey.get()}'")
        print(f"Stop hotkey set to '{self.stop_hotkey.get()}'")

# Run the Tkinter GUI
root = tk.Tk()
app = AutoClicker(root)
root.mainloop()
