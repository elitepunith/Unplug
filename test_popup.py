"""
standalone script that just shows the popup.
gets launched by the tray icon for testing.
also handy to run directly: py test_popup.py
"""

from config import load_settings
from sound import play_alert
from popup import ReminderPopup


def main():
    settings = load_settings()

    if settings["play_sound"]:
        play_alert(settings.get("sound_file", "alert.wav"))

    popup = ReminderPopup(
        reminders=settings["reminders"],
        timeout=settings["timeout_seconds"],
    )
    result = popup.show()
    print("result: {}".format(result))


if __name__ == "__main__":
    main()