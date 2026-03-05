import os
import sys

# winsound comes with windows python, no install needed
try:
    import winsound
    HAS_WINSOUND = True
except ImportError:
    HAS_WINSOUND = False


def play_alert(sound_file="alert.wav"):
    """plays a sound to grab attention. falls back to a beep if the wav is missing."""
    if not HAS_WINSOUND:
        return

    if getattr(sys, "frozen", False):
        base = os.path.dirname(sys.executable)
    else:
        base = os.path.dirname(os.path.abspath(__file__))

    full_path = os.path.join(base, sound_file)

    try:
        if os.path.isfile(full_path) and os.path.getsize(full_path) > 0:
            winsound.PlaySound(full_path, winsound.SND_FILENAME | winsound.SND_ASYNC)
        else:
            winsound.MessageBeep(winsound.MB_ICONEXCLAMATION)
    except Exception:
        pass  # not worth crashing over