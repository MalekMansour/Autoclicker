# Test File

# Author: Malek Mansour

import tkinter as tk
import threading
import time
import ctypes

# Low-level access for mouse events
SetCursorPos = ctypes.windll.user32.SetCursorPos
mouse_event = ctypes.windll.user32.mouse_event
MOUSEEVENTF_LEFTDOWN = 0x0002  
MOUSEEVENTF_LEFTUP = 0x0004   
MOUSEEVENTF_RIGHTDOWN = 0x0008  
MOUSEEVENTF_RIGHTUP = 0x0010    

class AutoClicker:
    def __init__(self, root):
        self.root = root
        self.root.title("AutoClicker")
        self.root.geometry("350x300")
        
        # Variables for click rate, button choice, and click status
        self.clicks_per_second = tk.DoubleVar(value=1.0)
        self.button_choice = tk.StringVar(value="left")
        self.running = False
        self.overlay_text = None

        # Clicks per second setting
        tk.Label(root, text="Clicks per Second:").pack(pady=5)
        tk.Entry(root, textvariable=self.clicks_per_second).pack()

        # Button choice setting (Left or Right click)
        tk.Label(root, text="Choose Button to Press:").pack(pady=5)
        button_options = tk.OptionMenu(root, self.button_choice, "left", "right")
        button_options.pack()

        # Start and Stop buttons
        tk.Button(root, text="Start (F2)", command=self.start_clicking).pack(pady=5)
        tk.Button(root, text="Stop (F3)", command=self.stop_clicking).pack(pady=5)

        # Bind hotkeys for starting and stopping
        root.bind("<F2>", lambda e: self.start_clicking())  # Start on F2
        root.bind("<F3>", lambda e: self.stop_clicking())   # Stop on F3
        root.bind("<Shift-KeyPress-Q>", lambda e: self.emergency_quit())  # Emergency quit

    def click_mouse(self):
        interval = 1 / self.clicks_per_second.get()  # Calculate interval from clicks per second
        self.show_status("Autoclicker: ON")
        
        while self.running:
            if self.button_choice.get() == "left":
                mouse_event(MOUSEEVENTF_LEFTDOWN, 0, 0, 0, 0)
                mouse_event(MOUSEEVENTF_LEFTUP, 0, 0, 0, 0)
            elif self.button_choice.get() == "right":
                mouse_event(MOUSEEVENTF_RIGHTDOWN, 0, 0, 0, 0)
                mouse_event(MOUSEEVENTF_RIGHTUP, 0, 0, 0, 0)
            time.sleep(interval)  # Wait based on clicks per second
        
        self.show_status("Autoclicker: OFF")

    def start_clicking(self):
        if not self.running:
            self.running = True
            threading.Thread(target=self.click_mouse).start()

    def stop_clicking(self):
        self.running = False

    def emergency_quit(self):
        """Immediately exits the program."""
        self.running = False
        self.root.quit()

    def show_status(self, text):
        """Display or update the autoclicker's status in a small, persistent overlay window."""
        if self.overlay_text is None:
            self.overlay_text = tk.Toplevel(self.root)
            self.overlay_text.overrideredirect(True)  # Remove window decorations
            self.overlay_text.geometry("+10+10")  # Position overlay at top-left corner
            label = tk.Label(self.overlay_text, text=text, font=("Arial", 12), fg="red", bg="white")
            label.pack()
        else:
            for widget in self.overlay_text.winfo_children():
                widget.config(text=text)

# Run the Tkinter GUI
root = tk.Tk()
app = AutoClicker(root)
root.mainloop()
