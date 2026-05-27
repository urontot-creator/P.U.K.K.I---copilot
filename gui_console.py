"""
P.U.K.K.I Console GUI
Real-time logging display with personality
"""

import tkinter as tk
from tkinter import scrolledtext
from datetime import datetime
import threading


class ConsoleGUI:
    """GUI console for P.U.K.K.I logs"""
    
    def __init__(self, width=350, height=500):
        self.window = tk.Tk()
        self.window.title("P.U.K.K.I Console")
        self.window.geometry(f"{width}x{height}")
        self.window.resizable(False, False)
        
        # Set dark theme
        self.window.configure(bg="#1e1e1e")
        
        # Status button (top)
        self.status_var = tk.StringVar(value="▶ START")
        self.status_btn = tk.Button(
            self.window,
            textvariable=self.status_var,
            font=("Courier", 10, "bold"),
            bg="#00AA00",
            fg="white",
            height=2,
            command=self.toggle_status
        )
        self.status_btn.pack(fill=tk.X, padx=5, pady=5)
        
        # Chat box (scrollable text area)
        self.chat_box = scrolledtext.ScrolledText(
            self.window,
            font=("Courier", 9),
            bg="#2d2d2d",
            fg="#00FF00",
            wrap=tk.WORD,
            state=tk.DISABLED,
            height=20
        )
        self.chat_box.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        # Configure text tags for different styles
        self.chat_box.tag_config("personality", foreground="#00FF00")  # Bright green
        self.chat_box.tag_config("system", foreground="#FFFF00")  # Yellow
        self.chat_box.tag_config("error", foreground="#FF0000")  # Red
        self.chat_box.tag_config("timestamp", foreground="#888888")  # Gray
        
        self.paused = False
        self.is_showing = False
        
    def log(self, message, style="personality"):
        """Add a log message to the console"""
        self.chat_box.config(state=tk.NORMAL)
        
        # Get timestamp
        timestamp = datetime.now().strftime("%H:%M")
        
        # Add timestamp
        self.chat_box.insert(tk.END, f"[{timestamp}] ", "timestamp")
        
        # Add message
        self.chat_box.insert(tk.END, message + "\n", style)
        
        # Auto scroll to latest
        self.chat_box.see(tk.END)
        self.chat_box.config(state=tk.DISABLED)
        
    def toggle_status(self):
        """Toggle START/PAUSE status"""
        if self.paused:
            self.status_var.set("⏸ PAUSE")
            self.status_btn.config(bg="#00AA00")
            self.paused = False
            self.log("P.U.K.K.I: Back to work! Resumed!", style="personality")
        else:
            self.status_var.set("▶ START")
            self.status_btn.config(bg="#AA0000")
            self.paused = True
            self.log("P.U.K.K.I: Taking a break... Paused!", style="system")
            
    def show(self):
        """Display the console window"""
        self.is_showing = True
        self.log("P.U.K.K.I: Initializing systems...", style="system")
        self.log("P.U.K.K.I: Ready to farm! Press START to begin.", style="personality")
        self.window.mainloop()
        
    def close(self):
        """Close the console window"""
        try:
            self.window.quit()
        except:
            pass
