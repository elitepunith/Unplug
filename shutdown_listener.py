import ctypes
import subprocess
import logging
import threading

try:
    import win32gui
    import win32con
    import win32api
    HAS_WIN32 = True
except ImportError:
    HAS_WIN32 = False

user32 = ctypes.windll.user32 if HAS_WIN32 else None
logger = logging.getLogger("shutdown_reminder")


class ShutdownListener:
    """
    hidden window that catches windows shutdown messages.
    blocks shutdown long enough to show the reminder popup,
    then either re-triggers shutdown or cancels it.
    """

    def __init__(self, on_shutdown_detected):
        if not HAS_WIN32:
            raise RuntimeError("need pywin32 — run: pip install pywin32")
        self.on_shutdown_detected = on_shutdown_detected
        self._hwnd = None
        self._class_atom = None
        self._shutdown_pending = False

    def start(self):
        logger.info("setting up shutdown listener")

        wc = win32gui.WNDCLASS()
        wc.lpfnWndProc = self._wnd_proc
        wc.lpszClassName = "UnplugHiddenWnd"
        wc.hInstance = win32api.GetModuleHandle(None)

        self._class_atom = win32gui.RegisterClass(wc)
        self._hwnd = win32gui.CreateWindow(
            self._class_atom, "UnplugHidden",
            0, 0, 0, 0, 0, 0, 0,
            wc.hInstance, None,
        )
        logger.info("listener ready (hwnd=%s)", self._hwnd)
        self._pump_messages()

    def _wnd_proc(self, hwnd, msg, wparam, lparam):
        if msg == win32con.WM_QUERYENDSESSION:
            logger.info("caught shutdown signal")

            try:
                user32.ShutdownBlockReasonCreate(
                    hwnd, "Checking your reminder list..."
                )
            except Exception as e:
                logger.warning("couldnt set block reason: %s" % e)

            if not self._shutdown_pending:
                self._shutdown_pending = True
                t = threading.Thread(target=self._popup_and_decide, daemon=True)
                t.start()

            return False  # block shutdown for now

        if msg == win32con.WM_ENDSESSION:
            logger.info("shutdown confirmed by windows")
            return 0

        if msg == win32con.WM_DESTROY:
            win32gui.PostQuitMessage(0)
            return 0

        return win32gui.DefWindowProc(hwnd, msg, wparam, lparam)

    def _popup_and_decide(self):
        try:
            allow = self.on_shutdown_detected()
        except Exception as e:
            logger.error("popup failed: %s" % e)
            allow = True  # dont trap the user if something breaks

        try:
            user32.ShutdownBlockReasonDestroy(self._hwnd)
        except Exception:
            pass

        self._shutdown_pending = False

        if allow:
            logger.info("proceeding with shutdown")
            try:
                subprocess.Popen(["shutdown", "/s", "/t", "0"])
            except Exception as e:
                logger.error("couldnt restart shutdown: %s" % e)
        else:
            logger.info("shutdown cancelled by user")

    def _pump_messages(self):
        win32gui.PumpMessages()