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

        # Clicks per second setting
        tk.Label(root, text="Clicks per Second:").pack(pady=5)
        tk.Entry(root, textvariable=self.clicks_per_second).pack()

        # Button choice setting (Left or Right click)
        tk.Label(root, text="Choose Button to Press:").pack(pady=5)
        button_options = tk.OptionMenu(root, self.button_choice, "left", "right")
        button_options.pack()

        # Hotkey settings for Start and Stop
        self.start_hotkey = tk.StringVar(value="s")  # Default start hotkey
        self.stop_hotkey = tk.StringVar(value="e")   # Default stop hotkey
        tk.Label(root, text="Start Hotkey:").pack(pady=5)
        tk.Entry(root, textvariable=self.start_hotkey).pack()
        tk.Label(root, text="Stop Hotkey:").pack(pady=5)
        tk.Entry(root, textvariable=self.stop_hotkey).pack()

        # Start and Stop buttons
        tk.Button(root, text="Start", command=self.start_clicking).pack(pady=5)
        tk.Button(root, text="Stop", command=self.stop_clicking).pack(pady=5)

        # Apply Hotkeys button
        tk.Button(root, text="Apply Hotkeys", command=self.apply_hotkeys).pack(pady=10)
        
        # Bind default hotkeys
        root.bind(f"<KeyPress-{self.start_hotkey.get()}>", lambda e: self.start_clicking())
        root.bind(f"<KeyPress-{self.stop_hotkey.get()}>", lambda e: self.stop_clicking())

        # Emergency quit hotkey: Shift+Q
        root.bind("<Shift-KeyPress-Q>", lambda e: self.emergency_quit())

        # Overlay window for status display
        self.status_window = tk.Toplevel(root)
        self.status_window.overrideredirect(True)  # Remove window decorations
        self.status_window.attributes("-topmost", True)  # Keep it on top
        self.status_window.geometry("150x30+10+10")  # Position in top-left corner
        self.status_window.configure(bg="black")
        
        # Status label with default setting
        self.status_label = tk.Label(self.status_window, text="Autoclicker: Off", font=("Arial", 12),
                                     bg="black", fg="lime")
        self.status_label.pack()
        self.status_window.withdraw()  # Hide initially

    def click_mouse(self):
        interval = 1 / self.clicks_per_second.get()  # Calculate interval from clicks per second
        while self.running:
            if interval > 0:  # Ensure interval is not zero
                if self.button_choice.get() == "left":
                    mouse_event(MOUSEEVENTF_LEFTDOWN, 0, 0, 0, 0)
                    time.sleep(0.01)  # Small delay for the click to register
                    mouse_event(MOUSEEVENTF_LEFTUP, 0, 0, 0, 0)
                elif self.button_choice.get() == "right":
                    mouse_event(MOUSEEVENTF_RIGHTDOWN, 0, 0, 0, 0)
                    time.sleep(0.01)  # Small delay for the click to register
                    mouse_event(MOUSEEVENTF_RIGHTUP, 0, 0, 0, 0)
                time.sleep(interval)  # Wait based on clicks per second
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

    def apply_hotkeys(self):
        # Rebind hotkeys based on user input
        self.root.bind(f"<KeyPress-{self.start_hotkey.get()}>", lambda e: self.start_clicking())
        self.root.bind(f"<KeyPress-{self.stop_hotkey.get()}>", lambda e: self.stop_clicking())
        print(f"Start hotkey set to '{self.start_hotkey.get()}'")
        print(f"Stop hotkey set to '{self.stop_hotkey.get()}'")

    def update_status(self, status_text):
        """Updates the status overlay with new text."""
        self.status_label.config(text=status_text)
        if status_text == "Autoclicker: On":
            self.status_window.deiconify()  # Show the window
        else:
            self.status_window.withdraw()  # Hide the window

    def emergency_quit(self):
        """Immediately exits the program."""
        self.running = False
        self.update_status("Autoclicker: Off")
        self.root.quit()

# Run the Tkinter GUI
root = tk.Tk()
app = AutoClicker(root)
root.mainloop()
