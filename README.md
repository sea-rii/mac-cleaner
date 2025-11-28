# 🍏 Mac Cleaner — by Sai Siri

A lightweight, safe, and smart macOS cleaning tool built in Python.  
This CLI-based utility helps you free space, clean old junk, scan for huge files, and visualize storage usage — all with a beautiful terminal UI powered by **Rich**.

✨ Perfect for keeping your Mac fast, organized, and clutter-free.


## 🚀 Features

### 🧹 Age-based cleaning
- Cleans only **old** cache and log files  
- Default threshold: **30 days**  
- Keeps recent files so apps don’t break  
- Safe and smart cleanup

### 🔍 Big File Radar
Scans your Mac for extremely large files in:
- `~/Downloads`
- `~/Desktop`
- `~/Movies`

Shows a clean table of the **top 20 largest files**, sorted by size.

### 📊 Space Dashboard
After a full clean, see:
- Cache size (before → after)
- Logs size (before → after)
- Total GB freed
- Neatly formatted Rich UI table

### 🎨 Fancy CLI UI
Powered by the `rich` library:
- Colors  
- Progress bars  
- Pretty tables  
- Clean output everywhere

### 🗑️ Trash Cleaning (via Finder)
Uses macOS AppleScript:
```bash
tell application "Finder" to empty trash
```

## ▶️ Usage
Run the tool:

> python main.py

Interactive menu:
```
1) Clean caches (age-based)
2) Clean logs (age-based)
3) Empty Trash (via Finder)
4) Big File Radar
5) FULL CLEAN + dashboard
6) Exit
```
Pick an option and let the cleaner work ✨

## ⚙️ Customization

Inside main.py, adjust:
> days_threshold=30        # Delete files older than this many days
> large_file_min_mb=500    # Big File Radar threshold

Examples:

Set days_threshold=7 for more aggressive weekly cleaning

Lower big file threshold to 200MB if you want a deeper scan


## 📂 Project Structure
```
mac-cleaner/
│── main.py               # App menu + logic
│── cleaner.py            # Core cleaner engine
│── utils.py              # Formatting helpers
│── venv/                 # Virtual environment (ignored)
│── .gitignore
│── README.md
```

## 🛡️ Safety

- Mac Cleaner v2 is built to be safe:
- Only touches user-level caches/logs
- Uses age-based deletion
- Skips protected macOS system folders
- Shows warnings for anything it can't access
- Trash is emptied using Finder instead of raw deletion

## 💛 Credits

Developed by: Sai Siri Chittineni\
Designed to keep your Mac light, clean, and speedy ✨
