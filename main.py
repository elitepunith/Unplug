"""
Shutdown Reminder
~~~~~~~~~~~~~~~~~
sits in your system tray, catches shutdown events, and shows you
a checklist popup before letting windows shut down. thats it.

usage:
    py main.py              (normal)
    pythonw.exe main.py     (no console window)
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
        self.logger.info("shutdown reminder started at {}".format(
            datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        ))
        self.logger.info("python {} on {}".format(sys.version, sys.platform))
        self.logger.info("=" * 50)

        if sys.platform != "win32":
            self.logger.error("this version only runs on windows")
            print("this build is windows-only.")
            sys.exit(1)

        # start the tray icon
        self.tray = TrayIcon(on_quit=self._quit)
        self.tray.start()
        self.logger.info("tray icon started")

        print("shutdown reminder is running")
        print("look for the icon in your system tray")
        print("right-click tray icon -> Test popup to try it")
        print("press ctrl+c to stop\n")

        # start listening for shutdown (this blocks)
        listener = ShutdownListener(on_shutdown_detected=self._handle_shutdown)
        try:
            listener.start()
        except RuntimeError as e:
            self.logger.error(str(e))
            print("FATAL: {}".format(e))
            sys.exit(1)
        except KeyboardInterrupt:
            self.logger.info("stopped")
            self._quit()

    def _handle_shutdown(self):
        """
        called when windows is trying to shut down.
        returns True (allow) or False (block).
        """
        self.logger.info("shutdown detected, showing popup")

        if self.settings["play_sound"]:
            play_alert(self.settings.get("sound_file", "alert.wav"))

        popup = ReminderPopup(
            reminders=self.settings["reminders"],
            timeout=self.settings["timeout_seconds"],
        )
        result = popup.show()

        self.logger.info("user chose: {}".format(result))
        return result == "proceed"

    def _quit(self):
        self.logger.info("quitting")
        if self.tray:
            self.tray.stop()
        os._exit(0)


if __name__ == "__main__":
    app = App()
    app.run()