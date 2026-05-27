# P.U.K.K.I - Clash of Clans Automation Bot
## Complete Setup Guide for Beginners

---

## 📋 What is P.U.K.K.I?
P.U.K.K.I is a Python automation bot that plays Clash of Clans for you:
- ✅ Upgrades walls automatically
- ✅ Farms resources by attacking bases
- ✅ Deploys troops strategically
- ✅ Has a personality and shows logs in real-time
- ✅ Runs on LD Player (Android emulator)

---

## 🛠️ Installation (Windows)

### 1. Make Sure Python is Installed
```bash
python --version
```
Should show something like `Python 3.10.0` or higher.

If not, download from: https://www.python.org/downloads/

### 2. Download This Project
- Go to your GitHub repo
- Click **Code** → **Download ZIP**
- Extract the folder somewhere safe

### 3. Open Command Prompt in Your Project Folder
- Right-click inside the folder
- Select **"Open in Terminal"** or **"Open Command Prompt here"**

### 4. Install Required Libraries
Copy and paste this command:
```bash
pip install -r requirements.txt
```

This downloads all the tools P.U.K.K.I needs. Wait 2-3 minutes.

---

## 📁 File Structure Setup

Create this folder structure in your project:

```
P.U.K.K.I---copilot/
├── pukki_main.py
├── bot_engine.py
├── gui_console.py
├── requirements.txt
├── walls.json
├── README_SETUP.md
│
└── templates/
    ├── home/
    │   └── builder.png
    │
    ├── wallupgrade/
    │   ├── goldupgrade.png
    │   ├── confirm_upgrade.png
    │   ├── no_gold.png
    │   ├── exit_upgrade_1.png
    │   └── exit_upgrade_2.png
    │
    ├── farm/
    │   ├── atk1a.png
    │   ├── atk1b.png
    │   ├── atk1c.png
    │   ├── atk1d.png
    │   ├── atk2.png
    │   ├── atk3.png
    │   └── cancel_search.png
    │
    ├── atk/
    │   ├── end_battle.png
    │   ├── return_home.png
    │   ├── surrender.png
    │   └── surrender_okay.png
    │
    └── unwantedpopups/
        ├── error_1.png
        ├── solution_1.png
        ├── error_2.png
        ├── solution_2.png
        └── ... (add more as needed)
```

---

## 📸 Taking Screenshots (Image Files)

You need to take screenshots of specific game screens. Here's how:

### For Each Image:
1. Open Clash of Clans on LD Player
2. Navigate to the screen you need
3. Press **Print Screen** button on keyboard
4. Open **Paint** (Windows)
5. Press **Ctrl + V** to paste
6. Save as `.png` file with the correct name

### What Each Image Is:

| Image Name | What to Screenshot | Notes |
|------------|------------------|-------|
| `builder.png` | Home screen with builder icon visible | - |
| `goldupgrade.png` | Gold upgrade button in wall upgrade menu | - |
| `confirm_upgrade.png` | Confirm/OK button to finalize upgrade | - |
| `no_gold.png` | Message saying "Not enough gold" | - |
| `exit_upgrade_1.png` | Exit/Cancel button (part 1) | - |
| `exit_upgrade_2.png` | Exit/Cancel button (part 2) | - |
| `atk1a.png`, `atk1b.png`, etc. | Attack button variant 1, 2, 3, 4 | Take all 4 variants |
| `atk2.png` | Attack confirmation button | - |
| `atk3.png` | Final attack start button | - |
| `cancel_search.png` | Cancel matchmaking button | - |
| `end_battle.png` | End battle button | - |
| `return_home.png` | Return home after battle button | - |
| `surrender.png` | Surrender button | - |
| `surrender_okay.png` | Confirm surrender button | - |

---

## ⚙️ Configuration

### Update walls.json
Open `walls.json` and set your current wall counts:

```json
{
  "lvl_15": 280,
  "lvl_16": 39,
  "lvl_17": 6,
  "lvl_18": 0
}
```

Get these numbers from your Clash of Clans home screen.

---

## 🎮 Running P.U.K.K.I

### Start the Bot:
```bash
python pukki_main.py
```

A console window appears with:
- **Green START button** at top
- **Log messages** in the chat area below

### Controls:
- **Click START** button to begin automation
- **Press Ctrl + P** to pause/resume anytime
- **Click START** button again to pause

### What You'll See:
```
[14:32] P.U.K.K.I: Initializing systems...
[14:32] P.U.K.K.I: Ready to farm! Press START to begin.
[14:33] P.U.K.K.I: Back to work! Resumed!
[14:33] P.U.K.K.I: Selecting Level 15 wall...
[14:34] P.U.K.K.I: Wall upgrade initiated!
[14:35] P.U.K.K.I: Farming time! Queuing up...
```

---

## 🐛 Troubleshooting

### Error: `ModuleNotFoundError: No module named 'cv2'`
→ Run: `pip install -r requirements.txt` again

### Error: `Template not found: templates/home/builder.png`
→ Make sure your image files are in the correct folders

### Bot doesn't click anything
→ Make sure LD Player window is in focus and at 720p resolution

### Bot pauses randomly
→ Check if you accidentally pressed Ctrl + P

---

## 📝 Important Notes

1. **LD Player must be at 720p resolution** - Bot is calibrated for this
2. **Game must be in focus** - Don't click on other windows while bot runs
3. **Image files must match exactly** - Names are case-sensitive
4. **walls.json must be accurate** - Or bot will skip needed upgrades

---

## 🎯 How It Works (Simple Version)

1. **Home Check** → Bot looks for home screen
2. **Wall Selection** → Picks best wall to upgrade (15→16→17→18)
3. **Upgrade** → Upgrades the wall with gold/elixir
4. **Farm Prep** → Queues up an attack match
5. **Deploy** → Sends electro dragons and other troops
6. **Return** → Goes back home after battle
7. **Repeat** → Steps 1-6 happen over and over

---

## 💡 Tips

- Let the bot run for a few minutes to test
- Watch the console to see what it's doing
- If something goes wrong, press Ctrl + P to pause
- Check image names - they must match exactly (case-sensitive)

---

## ✅ You're Ready!

Once you have:
1. ✅ All files downloaded
2. ✅ Libraries installed (`pip install -r requirements.txt`)
3. ✅ Screenshot images organized in `templates/` folder
4. ✅ `walls.json` updated with your wall counts

**Run:** `python pukki_main.py`

**Good luck! Let the automation begin!** 🚀
