# Unplug

A lightweight Windows 10/11 app that sits in your system tray and shows a reminder checklist when you shut down your PC.

## What it does

- Sits quietly in your system tray
- When you hit Shut Down / Restart, it intercepts the event
- Shows a popup with your custom checklist
- Plays a sound alert
- You can either proceed with or cancel the shutdown
- Auto-proceeds after the timeout (default 45 seconds)

## Setup

Requires Python 3.10+ and Windows 10/11.

```
pip install -r requirements.txt
python main.py
```

To run without the console window:

```
pythonw.exe main.py
```

## How to test

**Option 1 — tray menu**

Right-click the tray icon and choose **Test popup** to see the popup without actually shutting down.

**Option 2 — scheduled shutdown**

Open a command prompt as Administrator and run:

```
shutdown /s /t 120
```

This schedules a shutdown in 120 seconds. The app will intercept it and show the popup.
To cancel manually if needed: `shutdown /a`

## Build standalone .exe

Run:

```
build.bat
```

This installs dependencies, packages everything with PyInstaller, and creates `dist\Unplug.exe` — a single file, no Python needed.

## Auto-start on boot

1. Press Win+R, type `shell:startup`, hit Enter
2. Create a shortcut to `Unplug.exe` (or `pythonw.exe main.py`)
3. Drop it in that folder
4. Done — it'll start every time you log in

## Configuration

Edit `settings.json` to customise your reminders, timeout, and sound:

```json
{
    "reminders": [
        "Save all open files",
        "Push your git commits",
        "Close browser tabs you need later"
    ],
    "timeout_seconds": 45,
    "play_sound": true,
    "sound_file": "alert.wav",
    "log_file": "shutdown_reminder.log"
}
```

## Troubleshooting

- **No popup on shutdown**: Make sure the app is running (check the system tray icon)
- **pywin32 import error**: Run `pip install pywin32` then `python Scripts/pywin32_postinstall.py -install`
- **No tray icon**: Run `pip install pystray Pillow`
- **No sound**: Make sure `alert.wav` exists next to the app and is not 0 bytes, or set `play_sound` to `false`