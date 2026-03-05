import threading
import subprocess
import sys
import os

try:
    import pystray
    from PIL import Image, ImageDraw
    HAS_TRAY = True
except ImportError:
    HAS_TRAY = False


class TrayIcon:
    """
    little icon that sits in your system tray so you know
    the app is running. right-click gives you a menu to quit
    or show a test popup.
    """

    def __init__(self, on_quit=None, on_test_popup=None):
        self.on_quit = on_quit
        self.on_test_popup = on_test_popup
        self._icon = None

    def start(self):
        if not HAS_TRAY:
            print("[tray] pystray or Pillow not installed, skipping tray icon")
            return

        t = threading.Thread(target=self._run, daemon=True)
        t.start()

    def _run(self):
        image = self._load_icon()
        menu = pystray.Menu(
            pystray.MenuItem("Shutdown Reminder", None, enabled=False),
            pystray.Menu.SEPARATOR,
            pystray.MenuItem("Test popup", self._handle_test),
            pystray.MenuItem("Quit", self._handle_quit),
        )
        self._icon = pystray.Icon(
            "shutdown_reminder",
            image,
            "Shutdown Reminder - Running",
            menu,
        )
        self._icon.run()

    def _load_icon(self):
        if getattr(sys, "frozen", False):
            base = os.path.dirname(sys.executable)
        else:
            base = os.path.dirname(os.path.abspath(__file__))

        icon_path = os.path.join(base, "icon.png")

        try:
            if os.path.isfile(icon_path):
                img = Image.open(icon_path)
                img = img.resize((64, 64))
                return img
        except Exception:
            pass

        # fallback: make a simple bell-ish icon
        img = Image.new("RGB", (64, 64), "#db4b4b")
        draw = ImageDraw.Draw(img)
        draw.rectangle([16, 16, 48, 48], fill="#ffffff")
        draw.rectangle([28, 12, 36, 20], fill="#ffffff")
        return img

    def _handle_test(self, icon, item):
        """
        spawn the popup in a completely separate process.
        tkinter and threads dont mix well, this is the
        most reliable way to do it from a tray callback.
        """
        if getattr(sys, "frozen", False):
            script = os.path.join(os.path.dirname(sys.executable), "test_popup.py")
            python = sys.executable
        else:
            script = os.path.join(
                os.path.dirname(os.path.abspath(__file__)), "test_popup.py"
            )
            python = sys.executable

        try:
            subprocess.Popen([python, script])
        except Exception as e:
            print("[tray] failed to launch test popup: {}".format(e))
            # fallback: try the callback if one was set
            if self.on_test_popup:
                self.on_test_popup()

    def _handle_quit(self, icon, item):
        if self._icon:
            self._icon.stop()
        if self.on_quit:
            self.on_quit()

    def stop(self):
        if self._icon:
            try:
                self._icon.stop()
            except Exception:
                pass