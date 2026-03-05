import json
import os
import sys


DEFAULT_SETTINGS = {
    "reminders": ["Save all open files"],
    "timeout_seconds": 45,
    "play_sound": True,
    "sound_file": "alert.wav",
    "log_file": "shutdown_reminder.log",
}


def get_base_dir():
    """figure out where our files live, works both in dev and pyinstaller bundle"""
    if getattr(sys, "frozen", False):
        return os.path.dirname(sys.executable)
    return os.path.dirname(os.path.abspath(__file__))


def load_settings():
    path = os.path.join(get_base_dir(), "settings.json")
    try:
        with open(path, "r", encoding="utf-8") as f:
            data = json.load(f)
        # merge with defaults so missing keys dont blow up
        merged = dict(DEFAULT_SETTINGS)
        merged.update(data)
        return merged
    except FileNotFoundError:
        print("[config] settings.json not found, using defaults")
        return dict(DEFAULT_SETTINGS)
    except json.JSONDecodeError as e:
        print("[config] broken json in settings.json: {}".format(e))
        return dict(DEFAULT_SETTINGS)
    except Exception as e:
        print("[config] unexpected error loading settings: {}".format(e))
        return dict(DEFAULT_SETTINGS)