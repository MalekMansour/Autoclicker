# Autoclicker
# Author: Malek Mansour

import tkinter as tk
import pyautogui
import threading
import time

class AutoClicker:
    def __init__(self, root):
        self.root = root
        self.root.title("AutoClicker")
        self.root.geometry("300x150")
        
        # Variables for click interval and click status
        self.interval = tk.DoubleVar(value=1.0)
        self.running = False

        # Interval Label and Entry
        tk.Label(root, text="Click Interval (seconds):").pack(pady=5)
        tk.Entry(root, textvariable=self.interval).pack()

        # Start and Stop buttons
        self.start_button = tk.Button(root, text="Start", command=self.start_clicking)
        self.start_button.pack(pady=5)
        self.stop_button = tk.Button(root, text="Stop", command=self.stop_clicking)
        self.stop_button.pack(pady=5)

    def click_mouse(self):
        while self.running:
            pyautogui.click()  # Perform the mouse click
            time.sleep(self.interval.get())  # Wait for the specified interval

    def start_clicking(self):
        if not self.running:
            self.running = True
            thread = threading.Thread(target=self.click_mouse)
            thread.start()

    def stop_clicking(self):
        self.running = False

# Run the Tkinter GUI
root = tk.Tk()
app = AutoClicker(root)
root.mainloop()
