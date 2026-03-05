# Unplug

A tiny Windows app that reminds you to check things off before your PC shuts down.

Ever hit "Shut Down" and then realized you forgot to save something, push your code, or close those 47 browser tabs? Yeah, me too. That's why I made this.

## How it works

1. Runs quietly in your system tray
2. When you shut down or restart, it intercepts the event
3. Shows a popup with your personal checklist
4. You either confirm shutdown or cancel it
5. If you ignore it, it auto-proceeds after 45 seconds

That's it. Nothing fancy, nothing bloated.

## Getting started

You need Python 3.10+ on Windows 10 or 11.

```
pip install -r requirements.txt
python main.py
```

To run without the black console window popping up:

```
pythonw.exe main.py
```

## Make it your own

Edit `settings.json`:

```json
{
    "reminders": [
        "Save all open files",
        "Push your git commits",
        "Close browser tabs you need later",
        "Update your work log"
    ],
    "timeout_seconds": 45,
    "play_sound": true,
    "sound_file": "alert.wav",
    "log_file": "shutdown_reminder.log"
}
```

Add whatever reminders matter to you. Change the timeout. Turn off the sound if it annoys you.

## Building a standalone .exe

```
build.bat
```

This packages everything into a single `dist\Unplug.exe` file using PyInstaller. No Python installation needed to run it.

## Auto-start on login

1. Press `Win+R`, type `shell:startup`, hit Enter
2. Drop a shortcut to `Unplug.exe` in there
3. Done — starts every time you log in

## If something isn't working

- **No popup when you shut down** — make sure the app is actually running (check your system tray)
- **pywin32 errors** — run `pip install pywin32` then `python Scripts/pywin32_postinstall.py -install`
- **No tray icon** — `pip install pystray Pillow`
- **No sound** — check that `alert.wav` exists and isn't empty, or set `play_sound` to `false`

## License

Do whatever you want with it.