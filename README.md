# Shutdown Reminder

A lightweight Windows app that detects when you're shutting down your PC
and pops up a quick checklist to make sure you didn't forget anything.

## What it does

- Sits quietly in your system tray
- When you hit Shut Down / Restart, it intercepts the event
- Shows a popup with your custom checklist
- Plays a sound alert
- You can either proceed or cancel the shutdown
- Auto-proceeds after the timeout (default 45 seconds)

## Setup (from source)

You need Python 3.8 (the last version that supports Windows 7).

```
pip install -r requirements.txt
python main.py
```

To run without the console window:

```
pythonw.exe main.py
```

## Build standalone .exe

Just run:

```
build.bat
```

This creates `dist/ShutdownReminder.exe` — a single file, no Python needed.

## Configuration

Edit `settings.json` to change your reminders, timeout, sound, etc.

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

## Auto-start on boot

1. Press Win+R, type `shell:startup`, hit Enter
2. Create a shortcut to `ShutdownReminder.exe` (or `pythonw.exe main.py`)
3. Drop it in that folder
4. Done — it'll start every time you log in

## System tray

Right-click the tray icon for:
- **Test popup** — see what it looks like without actually shutting down
- **Quit** — stop the app

## How to test without actually shutting down

Option 1 — use the tray menu "Test popup"

Option 2 — open cmd as Administrator and run:
```
shutdown /s /t 60
```
This schedules a shutdown in 60 seconds. The app will intercept it.
To cancel manually if needed: `shutdown /a`

## Troubleshooting

Check `shutdown_reminder.log` for errors.

Common issues:
- **No popup on shutdown**: Make sure the app is actually running (check tray)
- **pywin32 import error**: Run `pip install pywin32` and then `python Scripts/pywin32_postinstall.py -install`
- **No tray icon**: Install pystray and Pillow: `pip install pystray Pillow`
- **No sound**: Make sure `alert.wav` exists next to the app, or set `play_sound` to false