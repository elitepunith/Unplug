import json
import os
import sys

DEFAULTS = {
    "reminders": ["Save all open files"],
    "timeout_seconds": 45,
    "play_sound": True,
    "sound_file": "alert.wav",
    "log_file": "shutdown_reminder.log",
}


def get_base_dir():
    # pyinstaller changes where files live
    if getattr(sys, "frozen", False):
        return os.path.dirname(sys.executable)
    return os.path.dirname(os.path.abspath(__file__))


def load_settings():
    path = os.path.join(get_base_dir(), "settings.json")
    try:
        with open(path, "r", encoding="utf-8") as f:
            data = json.load(f)
        merged = dict(DEFAULTS)
        merged.update(data)
        return merged
    except FileNotFoundError:
        print("[config] no settings.json found, going with defaults")
        return dict(DEFAULTS)
    except json.JSONDecodeError as e:
        print("[config] settings.json is broken: %s" % e)
        return dict(DEFAULTS)
    except Exception as e:
        print("[config] weird error: %s" % e)
        return dict(DEFAULTS)