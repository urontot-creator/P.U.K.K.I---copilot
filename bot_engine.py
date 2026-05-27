"""
Bot Engine - Core automation logic for P.U.K.K.I
Handles template matching, screen recognition, and automation sequences
"""

import cv2
import numpy as np
import pyautogui
import time
import json
from pathlib import Path
from datetime import datetime


class BotEngine:
    """Core bot automation engine"""
    
    def __init__(self):
        self.screen_width = 1280
        self.screen_height = 720
        self.template_path = Path("templates")
        self.walls_data = self.load_walls_data()
        self.state = "HOME"  # HOME, SELECTING_WALL, UPGRADING, FARMING, ATTACKING, RETURNING
        self.last_wall_level = None
        self.farm_sequence_count = 0
        self.error_check_timer = 0
        self.in_battle = False
        self.electro_deployed_time = None
        
    def load_walls_data(self):
        """Load walls.json configuration"""
        try:
            with open("walls.json", "r") as f:
                return json.load(f)
        except Exception as e:
            print(f"Error loading walls.json: {e}")
            return {"lvl_15": 0, "lvl_16": 0, "lvl_17": 0, "lvl_18": 0}
            
    def get_screen(self):
        """Capture current screen"""
        try:
            screenshot = pyautogui.screenshot(region=(0, 0, self.screen_width, self.screen_height))
            return cv2.cvtColor(np.array(screenshot), cv2.COLOR_RGB2BGR)
        except Exception as e:
            print(f"Error capturing screen: {e}")
            return None
            
    def find_template(self, template_name, threshold=0.8, scan_only=False):
        """
        Find a template image on screen
        
        Args:
            template_name: Name of template file (e.g., "home/builder.png")
            threshold: Matching threshold (0-1)
            scan_only: If True, only scan without clicking
            
        Returns:
            Tuple (x, y) if found, None otherwise
        """
        try:
            template_path = self.template_path / template_name
            if not template_path.exists():
                print(f"Template not found: {template_path}")
                return None
                
            screen = self.get_screen()
            template = cv2.imread(str(template_path))
            
            if screen is None or template is None:
                return None
                
            result = cv2.matchTemplate(screen, template, cv2.TM_CCOEFF)
            min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(result)
            
            # Normalize score to 0-1 range
            score = (max_val - min_val) / (max_val - min_val + 1e-5) if max_val > min_val else 0
            
            if score >= threshold:
                h, w = template.shape[:2]
                center_x = max_loc[0] + w // 2
                center_y = max_loc[1] + h // 2
                return (center_x, center_y)
                
            return None
        except Exception as e:
            print(f"Error in find_template: {e}")
            return None
            
    def click(self, x, y, delay=0.3):
        """Click at coordinates"""
        try:
            pyautogui.click(x, y)
            time.sleep(delay)
        except Exception as e:
            print(f"Error clicking: {e}")
            
    def press_key(self, key, delay=0.2):
        """Press a keyboard key"""
        try:
            pyautogui.press(key)
            time.sleep(delay)
        except Exception as e:
            print(f"Error pressing key: {e}")
            
    def release_mouse(self):
        """Release mouse control"""
        try:
            pyautogui.moveTo(10, 10)
        except:
            pass
            
    def check_home_screen(self, console):
        """Check if on home screen (Step 1)"""
        home_found = self.find_template("home/builder.png", threshold=0.75)
        
        if home_found:
            self.state = "HOME"
            return True
        else:
            console.log("P.U.K.K.I: Where am I? Home not detected!", style="error")
            return False
            
    def select_wall_to_upgrade(self, console):
        """Smart wall selection based on levels (Step 2)"""
        walls = self.walls_data
        
        # Check for walls to upgrade
        if walls["lvl_15"] > 0:
            self.press_key("m")
            selected = "Level 15"
        elif walls["lvl_16"] > 0:
            self.press_key("n")
            selected = "Level 16"
        elif walls["lvl_17"] > 0:
            self.press_key("b")
            selected = "Level 17"
        elif walls["lvl_18"] > 0:
            self.press_key("v")
            selected = "Level 18"
        else:
            console.log("P.U.K.K.I: Look at that, we're all maxed out!", style="personality")
            self.state = "FARM_PREP"
            return False
            
        # Click builder icon for UI reasons
        builder = self.find_template("home/builder.png")
        if builder:
            self.click(builder[0], builder[1], delay=0.5)
            
        console.log(f"P.U.K.K.I: Selecting {selected} wall...", style="personality")
        self.state = "WALL_SELECTED"
        time.sleep(1)
        return True
        
    def upgrade_wall(self, console):
        """Attempt wall upgrade (Step 3)"""
        # Try gold upgrade
        gold_upgrade = self.find_template("wallupgrade/goldupgrade.png", threshold=0.75)
        
        if gold_upgrade:
            self.click(gold_upgrade[0], gold_upgrade[1])
            time.sleep(0.5)
            
            # Click confirm
            confirm = self.find_template("wallupgrade/confirm_upgrade.png", threshold=0.75)
            if confirm:
                self.click(confirm[0], confirm[1])
                console.log("P.U.K.K.I: Wall upgrade initiated!", style="personality")
                self.state = "UPGRADING"
                time.sleep(2)
                return True
                
        # Check for insufficient resources
        no_gold = self.find_template("wallupgrade/no_gold.png", threshold=0.75)
        no_elix = self.find_template("wallupgrade/no_elix.png", threshold=0.75)
        
        if no_gold or no_elix:
            console.log("P.U.K.K.I: Crap!! We ran out of loot.", style="personality")
            # Exit upgrade
            exit1 = self.find_template("wallupgrade/exit_upgrade_1.png")
            if exit1:
                self.click(exit1[0], exit1[1])
            self.state = "FARM_PREP"
            self.farm_sequence_count = 0
            return False
            
        return False
        
    def farm_prep(self, console):
        """Prepare for farming - enter matchmaking (Step 4)"""
        console.log("P.U.K.K.I: Farming time! Queuing up...", style="personality")
        
        # Click attack button 1
        for atk_variant in ["atk1a.png", "atk1b.png", "atk1c.png", "atk1d.png"]:
            atk1 = self.find_template(f"farm/{atk_variant}", threshold=0.75)
            if atk1:
                self.click(atk1[0], atk1[1])
                break
                
        time.sleep(1)
        
        # Click attack button 2
        atk2 = self.find_template("farm/atk2.png", threshold=0.75)
        if atk2:
            self.click(atk2[0], atk2[1])
            time.sleep(1)
            
        # Click attack button 3
        atk3 = self.find_template("farm/atk3.png", threshold=0.75)
        if atk3:
            self.click(atk3[0], atk3[1])
            time.sleep(2)
            
        # Wait for battle to start (scan for end_battle.png as indicator)
        start_time = time.time()
        while time.time() - start_time < 40:
            end_battle = self.find_template("atk/end_battle.png", threshold=0.75)
            if end_battle:
                console.log("P.U.K.K.I: Battle found! Deploying troops...", style="personality")
                self.state = "ATTACKING"
                self.in_battle = True
                self.electro_deployed_time = None
                return True
            time.sleep(1)
            
        # Timeout - cancel search and return home
        console.log("P.U.K.K.I: Matchmaking took too long. Canceling...", style="error")
        cancel = self.find_template("farm/cancel_search.png", threshold=0.75)
        if cancel:
            self.click(cancel[0], cancel[1])
            
        self.state = "HOME"
        return False
        
    def deploy_troops(self, console):
        """Deploy troops in battle (Step 5)"""
        # This is a simplified version - actual deployment needs hero detection
        console.log("P.U.K.K.I: Electro Dragons incoming!", style="personality")
        
        # Deploy 10 Electro Dragons
        self.press_key("q")  # Select Electro Dragons
        time.sleep(0.3)
        
        for key in "1234567890":
            self.press_key(key)
            time.sleep(0.2)
            
        time.sleep(1)
        
        # Deploy Siege Machine
        self.press_key("w")
        time.sleep(0.3)
        self.press_key("5")
        time.sleep(1)
        
        console.log("P.U.K.K.I: Siege Machine deployed!", style="personality")
        
        # Record deployment time for 90s timer
        self.electro_deployed_time = time.time()
        self.state = "WAITING_RETURN"
        return True
        
    def check_return_home(self, console):
        """Check for battle end and return home (Step 6)"""
        # Case 1: Check for return home button (best case - quick win)
        return_home = self.find_template("atk/return_home.png", threshold=0.75)
        if return_home:
            self.click(return_home[0], return_home[1])
            console.log("P.U.K.K.I: Victory! Heading home...", style="personality")
            self.state = "HOME"
            return True
            
        # Case 2: 90 second timer reached - force end
        if self.electro_deployed_time:
            elapsed = time.time() - self.electro_deployed_time
            if elapsed > 90:
                console.log("P.U.K.K.I: Time's up! Battle done, going home...", style="personality")
                
                # Click end battle or surrender
                end_battle = self.find_template("atk/end_battle.png", threshold=0.75)
                if end_battle:
                    self.click(end_battle[0], end_battle[1])
                    time.sleep(0.5)
                else:
                    surrender = self.find_template("atk/surrender.png", threshold=0.75)
                    if surrender:
                        self.click(surrender[0], surrender[1])
                        time.sleep(0.5)
                        
                # Confirm surrender
                confirm = self.find_template("atk/surrender_okay.png", threshold=0.75)
                if confirm:
                    self.click(confirm[0], confirm[1])
                    
                self.state = "HOME"
                return True
                
        return False
        
    def error_handling(self, console):
        """Passively scan for and handle errors (Special 2)"""
        self.error_check_timer += 1
        
        if self.error_check_timer < 20:  # Check every 20 cycles
            return
            
        self.error_check_timer = 0
        
        # Scan for error popups
        for i in range(1, 6):  # Check error_1 through error_5
            error_template = f"unwantedpopups/error_{i}.png"
            solution_template = f"unwantedpopups/solution_{i}.png"
            
            error_found = self.find_template(error_template, threshold=0.75)
            if error_found:
                console.log(f"P.U.K.K.I: Found error popup! Fixing...", style="error")
                
                # Click solution
                solution = self.find_template(solution_template, threshold=0.75)
                if solution:
                    self.click(solution[0], solution[1])
                    console.log("P.U.K.K.I: Error fixed! Recalibrating...", style="system")
                    time.sleep(1)
                    
                    # Force reset to home
                    self.state = "HOME"
                    return
                    
    def run_cycle(self, console):
        """Run one complete bot cycle"""
        try:
            # Error handling (runs passively)
            self.error_handling(console)
            
            if self.state == "HOME":
                if self.check_home_screen(console):
                    self.select_wall_to_upgrade(console)
                    
            elif self.state == "WALL_SELECTED":
                if self.upgrade_wall(console):
                    pass
                else:
                    self.farm_prep(console)
                    
            elif self.state == "FARM_PREP":
                self.farm_prep(console)
                
            elif self.state == "ATTACKING":
                self.deploy_troops(console)
                
            elif self.state == "WAITING_RETURN":
                self.check_return_home(console)
                
            time.sleep(0.5)
            
        except Exception as e:
            console.log(f"ERROR: {str(e)}", style="error")
            self.state = "HOME"
