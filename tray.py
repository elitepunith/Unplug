import threading
import sys
import os

try:
    import pystray
    from PIL import Image, ImageDraw
    HAS_TRAY = True
except ImportError:
    HAS_TRAY = False


class TrayIcon:
    """system tray icon — just shows the app is alive, and lets you quit."""

    def __init__(self, on_quit=None):
        self.on_quit = on_quit
        self._icon = None

    def start(self):
        if not HAS_TRAY:
            print("[tray] pystray/Pillow missing, no tray icon for you")
            return
        threading.Thread(target=self._run, daemon=True).start()

    def _run(self):
        img = self._load_icon()
        menu = pystray.Menu(
            pystray.MenuItem("Unplug", None, enabled=False),
            pystray.Menu.SEPARATOR,
            pystray.MenuItem("Quit", self._on_quit),
        )
        self._icon = pystray.Icon("unplug", img, "Unplug — Running", menu)
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
                return img.resize((64, 64))
        except Exception:
            pass

        # fallback — quick and dirty placeholder
        img = Image.new("RGB", (64, 64), "#db4b4b")
        d = ImageDraw.Draw(img)
        d.rectangle([16, 16, 48, 48], fill="#ffffff")
        d.rectangle([28, 12, 36, 20], fill="#ffffff")
        return img

    def _on_quit(self, icon, item):
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