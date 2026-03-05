import os
import sys

# winsound is stdlib on windows, no pip install needed
try:
    import winsound
    HAS_WINSOUND = True
except ImportError:
    HAS_WINSOUND = False


def play_alert(sound_file="alert.wav"):
    """
    play the alert sound. if the wav file exists, use it.
    otherwise fall back to the default windows beep.
    nothing fancy, just needs to grab attention.
    """
    if not HAS_WINSOUND:
        return

    if getattr(sys, "frozen", False):
        base = os.path.dirname(sys.executable)
    else:
        base = os.path.dirname(os.path.abspath(__file__))

    full_path = os.path.join(base, sound_file)

    try:
        if os.path.isfile(full_path):
            winsound.PlaySound(full_path, winsound.SND_FILENAME | winsound.SND_ASYNC)
        else:
            # three quick beeps if no wav file found
            winsound.MessageBeep(winsound.MB_ICONEXCLAMATION)
    except Exception:
        # if sound fails, oh well, not the end of the world
        pass