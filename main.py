"""
Unplug — shutdown reminder for windows

catches the shutdown event and throws a checklist in your face
so you dont forget stuff. been there too many times.

run it:
    py main.py
    pythonw.exe main.py   (hides the console)
"""

import sys
import os
import logging
from datetime import datetime

from config import load_settings, get_base_dir
from popup import ReminderPopup
from sound import play_alert
from tray import TrayIcon
from shutdown_listener import ShutdownListener


def setup_logging(log_file):
    log_path = os.path.join(get_base_dir(), log_file)
    logging.basicConfig(
        filename=log_path,
        level=logging.INFO,
        format="%(asctime)s %(levelname)s %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
    )
    # also print to console so we can see whats happening
    console = logging.StreamHandler()
    console.setLevel(logging.INFO)
    console.setFormatter(logging.Formatter("%(asctime)s %(message)s", "%H:%M:%S"))
    logging.getLogger("shutdown_reminder").addHandler(console)


class App:
    def __init__(self):
        self.settings = load_settings()
        self.logger = logging.getLogger("shutdown_reminder")
        self.tray = None

    def run(self):
        setup_logging(self.settings["log_file"])

        self.logger.info("=" * 50)
        self.logger.info("started at %s", datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
        self.logger.info("python %s on %s", sys.version, sys.platform)
        self.logger.info("=" * 50)

        if sys.platform != "win32":
            self.logger.error("windows only, sorry")
            print("this only works on windows.")
            sys.exit(1)

        # tray icon so you know its running
        self.tray = TrayIcon(on_quit=self._quit)
        self.tray.start()
        self.logger.info("tray icon up")

        print("unplug is running — check your system tray")
        print("press ctrl+c to stop\n")

        # this blocks until the app is closed
        listener = ShutdownListener(on_shutdown_detected=self._handle_shutdown)
        try:
            listener.start()
        except RuntimeError as e:
            self.logger.error(str(e))
            print("FATAL: %s" % e)
            sys.exit(1)
        except KeyboardInterrupt:
            self.logger.info("stopped by user")
            self._quit()

    def _handle_shutdown(self):
        self.logger.info("shutdown detected — showing popup")

        if self.settings["play_sound"]:
            play_alert(self.settings.get("sound_file", "alert.wav"))

        popup = ReminderPopup(
            reminders=self.settings["reminders"],
            timeout=self.settings["timeout_seconds"],
        )
        result = popup.show()
        self.logger.info("user picked: %s", result)
        return result == "proceed"

    def _quit(self):
        self.logger.info("shutting down unplug")
        if self.tray:
            self.tray.stop()
        os._exit(0)


if __name__ == "__main__":
    App().run()