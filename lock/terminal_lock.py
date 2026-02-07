import tkinter as tk
from tkinter import messagebox
import pyautogui
import cv2
import threading
import winsound
import time
import os
import sys
import keyboard  # NEW: Library to block system keys

# --- CONFIGURATION ---
TERMINAL_BLACK = "#000000"
TERMINAL_GREEN = "#00FF00"
TERMINAL_RED = "#FF0000"
FONT_MAIN = ("Courier New", 14)
FONT_HEADER = ("Courier New", 20, "bold")
FONT_ALERT = ("Courier New", 35, "bold")

class TerminalSentry:
    def __init__(self, root):
        self.root = root
        self.root.title("TERMINAL_ACCESS_V2.0")
        self.root.geometry("600x400")
        self.root.configure(bg=TERMINAL_BLACK)
        
        self.password = ""
        self.is_armed = False
        self.start_mouse_pos = None
        self.alarm_active = False
        
        # --- UI SETUP ---
        header_text = """
> SYSTEM INTEGRITY: 100%
> KEYBOARD INTERCEPTOR: READY
> CAMERA MODULE: READY
-------------------------------------
> SENTRY TERMINAL v2.0 (LOCKED MODE)
> AWAITING INPUT...
-------------------------------------
"""
        tk.Label(root, text=header_text, font=FONT_MAIN, fg=TERMINAL_GREEN, bg=TERMINAL_BLACK, justify="left").pack(pady=(10, 20), anchor="w", padx=20)
        
        tk.Label(root, text="> SET SESSION PASSWORD:", font=FONT_MAIN, fg=TERMINAL_GREEN, bg=TERMINAL_BLACK).pack(anchor="w", padx=20)
        
        self.pass_entry = tk.Entry(root, show="*", font=FONT_MAIN, bg=TERMINAL_BLACK, fg=TERMINAL_GREEN, 
                                   insertbackground=TERMINAL_GREEN, relief=tk.FLAT, highlightthickness=1, highlightcolor=TERMINAL_GREEN)
        self.pass_entry.pack(pady=5, padx=20, fill="x")
        self.pass_entry.focus_set()
        
        self.arm_label = tk.Label(root, text="[ > INITIATE LOCKDOWN SEQUENCE < ]", font=FONT_HEADER, fg=TERMINAL_GREEN, bg=TERMINAL_BLACK, cursor="hand2")
        self.arm_label.pack(pady=40)
        self.arm_label.bind("<Button-1>", self.start_arming_sequence)
        
        # Hover effects
        self.arm_label.bind("<Enter>", lambda e: self.arm_label.config(fg=TERMINAL_BLACK, bg=TERMINAL_GREEN))
        self.arm_label.bind("<Leave>", lambda e: self.arm_label.config(fg=TERMINAL_GREEN, bg=TERMINAL_BLACK))

    def start_arming_sequence(self, event=None):
        self.password = self.pass_entry.get()
        if not self.password:
            messagebox.showerror("ERR", "> PASSWORD_REQUIRED")
            return
            
        self.pass_entry.delete(0, tk.END)
        self.arm_label.config(text="> ARMING IN 5 SECONDS...", fg=TERMINAL_GREEN, bg=TERMINAL_BLACK)
        self.root.update()
        
        # Hide window immediately
        self.root.withdraw()
        threading.Thread(target=self.arming_timer).start()

    def arming_timer(self):
        time.sleep(5)
        self.start_mouse_pos = pyautogui.position()
        self.is_armed = True
        self.monitor_mouse()

    def monitor_mouse(self):
        while self.is_armed:
            current_x, current_y = pyautogui.position()
            start_x, start_y = self.start_mouse_pos
            if abs(current_x - start_x) > 5 or abs(current_y - start_y) > 5:
                self.trigger_alarm()
                break
            time.sleep(0.1)

    def trigger_alarm(self):
        self.is_armed = False
        self.alarm_active = True
        
        # 1. BLOCK KEYBOARD INPUTS (The Trap)
        self.block_controls()
        
        # 2. Capture Photo
        threading.Thread(target=self.capture_intruder).start()
        
        # 3. Launch Red Screen
        self.root.after(0, self.show_red_terminal)
        
        # 4. Start Sound
        threading.Thread(target=self.play_alarm_sound, daemon=True).start()

    def block_controls(self):
        """Blocks common escape keys."""
        try:
            # Block Alt+Tab, Windows Key, etc.
            keyboard.block_key('alt')
            keyboard.block_key('tab')
            keyboard.block_key('windows')
            keyboard.block_key('esc')
            # Note: Ctrl+Alt+Del cannot be blocked by Python (System Safety Feature)
        except Exception as e:
            print(f"Could not block keys (Admin rights needed?): {e}")

    def unblock_controls(self):
        """Releases the keyboard blocks."""
        try:
            keyboard.unhook_all()
        except:
            pass

    def capture_intruder(self):
        try:
            cam = cv2.VideoCapture(0)
            time.sleep(1)
            ret, frame = cam.read()
            if ret:
                timestamp = time.strftime("%Y%m%d_%H%M%S")
                filename = f"INTRUDER_{timestamp}.jpg"
                cv2.imwrite(filename, frame)
            cam.release()
        except Exception:
            pass

    def play_alarm_sound(self):
        while self.alarm_active:
            winsound.Beep(2500, 800) 
            time.sleep(0.1)

    def show_red_terminal(self):
        self.lock_window = tk.Toplevel(self.root)
        self.lock_window.attributes("-fullscreen", True)
        self.lock_window.attributes("-topmost", True)
        self.lock_window.configure(bg=TERMINAL_BLACK, cursor="none")
        self.lock_window.protocol("WM_DELETE_WINDOW", lambda: None) # Disable 'X' button

        # Force focus repeatedly to prevent clicking away
        self.lock_window.after(500, self.force_focus)

        alert_text = """
> CRITICAL ALERT!
> UNAUTHORIZED PHYSICAL ACCESS DETECTED.
> SYSTEM CONTROLS: DISABLED
> ESCAPE KEYS: BLOCKED
-------------------------------------------
"""
        tk.Label(self.lock_window, text=alert_text, font=FONT_MAIN, fg=TERMINAL_RED, bg=TERMINAL_BLACK, justify="left").pack(pady=50)
        
        tk.Label(self.lock_window, text="> ENTER OVERRIDE CODE:", font=FONT_ALERT, fg=TERMINAL_RED, bg=TERMINAL_BLACK).pack(pady=20)
        
        self.unlock_entry = tk.Entry(self.lock_window, show="*", font=FONT_ALERT, bg=TERMINAL_BLACK, fg=TERMINAL_RED,
                                     insertbackground=TERMINAL_RED, relief=tk.FLAT, justify="center")
        self.unlock_entry.pack(pady=10, ipadx=10, ipady=10)
        self.unlock_entry.focus_set()
        self.unlock_entry.bind('<Return>', self.check_unlock)

    def force_focus(self):
        """Keeps the window on top aggressively."""
        if self.alarm_active:
            self.lock_window.attributes("-topmost", True)
            self.lock_window.focus_force()
            self.unlock_entry.focus_set()
            self.lock_window.after(500, self.force_focus)

    def check_unlock(self, event=None):
        user_input = self.unlock_entry.get()
        if user_input == self.password:
            # SUCCESS
            self.alarm_active = False
            self.unblock_controls()  # FREE THE KEYBOARD
            self.lock_window.destroy()
            self.root.deiconify()
            self.pass_entry.delete(0, tk.END)
            self.arm_label.config(text="[ > SYSTEM UNLOCKED - STANDBY < ]", fg=TERMINAL_GREEN, bg=TERMINAL_BLACK)
        else:
            # FAILURE
            self.unlock_entry.delete(0, tk.END)
            self.flash_red()

    def flash_red(self):
        self.unlock_entry.config(bg=TERMINAL_RED, fg=TERMINAL_BLACK)
        self.lock_window.update()
        time.sleep(0.2)
        self.unlock_entry.config(bg=TERMINAL_BLACK, fg=TERMINAL_RED)

if __name__ == "__main__":
    root = tk.Tk()
    app = TerminalSentry(root)
    root.mainloop()