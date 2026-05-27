"""
P.U.K.K.I - Clash of Clans Automation Bot
Main Entry Point
"""

import sys
import threading
import time
from pynput import keyboard
from gui_console import ConsoleGUI
from bot_engine import BotEngine


class PUKKIController:
    """Main controller for P.U.K.K.I bot"""
    
    def __init__(self):
        self.running = False
        self.paused = False
        self.bot = BotEngine()
        self.console = ConsoleGUI()
        self.bot_thread = None
        
    def toggle_pause(self):
        """Toggle pause/resume with Ctrl+P"""
        self.paused = not self.paused
        if self.paused:
            self.console.log("P.U.K.K.I: Taking a break... Paused!", style="system")
            self.bot.release_mouse()
        else:
            self.console.log("P.U.K.K.I: Back to work! Resumed!", style="system")
            
    def on_press(self, key):
        """Keyboard event handler"""
        try:
            if key == keyboard.Key.ctrl_l or key == keyboard.Key.ctrl_r:
                # Check if P is pressed while Ctrl is held
                pass
        except AttributeError:
            if hasattr(key, 'char') and key.char == 'p':
                # This would need better handling in actual implementation
                pass
                
    def run_bot(self):
        """Run the bot in a separate thread"""
        self.running = True
        self.console.log("P.U.K.K.I: Waking up! Starting automation...", style="personality")
        
        try:
            while self.running:
                if not self.paused:
                    # Main bot loop
                    self.bot.run_cycle(self.console)
                else:
                    time.sleep(0.5)
        except Exception as e:
            self.console.log(f"ERROR: {str(e)}", style="error")
            self.console.log("P.U.K.K.I: Uh oh... something broke!", style="error")
            
    def start(self):
        """Start P.U.K.K.I"""
        self.console.log("P.U.K.K.I: Initializing systems...", style="system")
        
        # Start bot thread
        self.bot_thread = threading.Thread(target=self.run_bot, daemon=True)
        self.bot_thread.start()
        
        # Start listening for Ctrl+P
        self.setup_hotkeys()
        
        # Show console
        self.console.show()
        
    def setup_hotkeys(self):
        """Setup global hotkey listener"""
        def on_press(key):
            try:
                if key == keyboard.Key.ctrl and hasattr(self, 'ctrl_pressed'):
                    self.ctrl_pressed = True
            except:
                pass
                
        def on_release(key):
            try:
                if key == keyboard.Key.ctrl:
                    self.ctrl_pressed = False
                elif hasattr(key, 'char') and key.char == 'p' and getattr(self, 'ctrl_pressed', False):
                    self.toggle_pause()
            except:
                pass
                
        listener = keyboard.Listener(on_press=on_press, on_release=on_release)
        listener.start()
        
    def stop(self):
        """Stop P.U.K.K.I"""
        self.running = False
        self.console.log("P.U.K.K.I: Shutting down... See you later!", style="personality")


if __name__ == "__main__":
    controller = PUKKIController()
    controller.start()
