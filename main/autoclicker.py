# Autoclicker
# Author: Malek Mansour
import tkinter as tk
import threading
import time
import keyboard  

class AutoClicker:
    def __init__(self, root):
        self.root = root
        self.root.title("AutoClicker")
        self.root.geometry("350x200")

        # Variables for click interval, click status, and hotkeys
        self.interval = tk.DoubleVar(value=1.0)
        self.running = False
        self.start_hotkey = tk.StringVar(value="s")  # Default start hotkey
        self.stop_hotkey = tk.StringVar(value="e")   # Default stop hotkey

        # Interval setting
        tk.Label(root, text="Click Interval (seconds):").pack(pady=5)
        tk.Entry(root, textvariable=self.interval).pack()

        # Hotkey settings for Start
        tk.Label(root, text="Start Hotkey:").pack(pady=5)
        tk.Entry(root, textvariable=self.start_hotkey).pack()

        # Hotkey settings for Stop
        tk.Label(root, text="Stop Hotkey:").pack(pady=5)
        tk.Entry(root, textvariable=self.stop_hotkey).pack()

        # Start and Stop buttons
        tk.Button(root, text="Apply Hotkeys", command=self.apply_hotkeys).pack(pady=10)

    def click_mouse(self):
        while self.running:
            pyautogui.click()  # Perform the mouse click
            time.sleep(self.interval.get())  # Wait for the specified interval

    def start_clicking(self):
        if not self.running:
            self.running = True
            threading.Thread(target=self.click_mouse).start()

    def stop_clicking(self):
        self.running = False

    def apply_hotkeys(self):
        # Unregister previous hotkeys if they exist
        keyboard.unhook_all_hotkeys()

        # Register new hotkeys from user input
        keyboard.add_hotkey(self.start_hotkey.get(), self.start_clicking)
        keyboard.add_hotkey(self.stop_hotkey.get(), self.stop_clicking)

        # Update the labels to confirm hotkey application
        print(f"Start hotkey set to '{self.start_hotkey.get()}'")
        print(f"Stop hotkey set to '{self.stop_hotkey.get()}'")

# Run the Tkinter GUI
root = tk.Tk()
app = AutoClicker(root)
root.mainloop()
