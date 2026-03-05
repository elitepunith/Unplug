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
    creates a hidden window that receives windows messages.
    when windows sends WM_QUERYENDSESSION we block it temporarily,
    show the popup in a separate thread, then either re-initiate
    shutdown or cancel it based on user choice.
    """

    def __init__(self, on_shutdown_detected):
        if not HAS_WIN32:
            raise RuntimeError("pywin32 is required. run: pip install pywin32")
        self.on_shutdown_detected = on_shutdown_detected
        self._hwnd = None
        self._class_atom = None
        self._shutdown_pending = False

    def start(self):
        logger.info("registering shutdown listener window")

        wc = win32gui.WNDCLASS()
        wc.lpfnWndProc = self._wnd_proc
        wc.lpszClassName = "ShutdownReminderHiddenWnd"
        wc.hInstance = win32api.GetModuleHandle(None)

        self._class_atom = win32gui.RegisterClass(wc)
        self._hwnd = win32gui.CreateWindow(
            self._class_atom,
            "ShutdownReminderHidden",
            0, 0, 0, 0, 0, 0, 0,
            wc.hInstance,
            None,
        )

        logger.info("hidden window created (hwnd={})".format(self._hwnd))
        self._pump_messages()

    def _wnd_proc(self, hwnd, msg, wparam, lparam):
        if msg == win32con.WM_QUERYENDSESSION:
            logger.info("WM_QUERYENDSESSION received")

            # tell windows we need more time to show a dialog
            try:
                user32.ShutdownBlockReasonCreate(
                    hwnd, "Checking your reminder list..."
                )
            except Exception as e:
                logger.warning("ShutdownBlockReasonCreate failed: {}".format(e))

            # show popup in a background thread so we return immediately
            if not self._shutdown_pending:
                self._shutdown_pending = True
                t = threading.Thread(target=self._show_popup_and_decide, daemon=True)
                t.start()

            # return False to block shutdown while we show the popup
            return False

        if msg == win32con.WM_ENDSESSION:
            logger.info("WM_ENDSESSION received, shutdown is happening")
            return 0

        if msg == win32con.WM_DESTROY:
            win32gui.PostQuitMessage(0)
            return 0

        return win32gui.DefWindowProc(hwnd, msg, wparam, lparam)

    def _show_popup_and_decide(self):
        try:
            allow = self.on_shutdown_detected()
        except Exception as e:
            logger.error("popup callback failed: {}".format(e))
            allow = True

        # clean up the block reason
        try:
            user32.ShutdownBlockReasonDestroy(self._hwnd)
        except Exception:
            pass

        self._shutdown_pending = False

        if allow:
            logger.info("user said proceed, re-initiating shutdown")
            try:
                subprocess.Popen(["shutdown", "/s", "/t", "0"])
            except Exception as e:
                logger.error("failed to re-initiate shutdown: {}".format(e))
        else:
            logger.info("user said cancel, blocking shutdown")
            self._cancel_shutdown()

    def _pump_messages(self):
        logger.info("message pump started")
        try:
            while True:
                win32gui.PumpWaitingMessages()
                time.sleep(0.1)
        except KeyboardInterrupt:
            logger.info("stopped by ctrl+c")
            self.stop()

    def _cancel_shutdown(self):
        try:
            result = subprocess.run(
                ["shutdown", "/a"],
                capture_output=True,
                timeout=5,
            )
            if result.returncode == 0:
                logger.info("shutdown cancelled successfully")
            else:
                logger.warning("shutdown /a returned code {}".format(result.returncode))
        except subprocess.TimeoutExpired:
            logger.warning("shutdown /a timed out")
        except FileNotFoundError:
            logger.error("shutdown command not found")
        except Exception as e:
            logger.error("failed to cancel shutdown: {}".format(e))

    def stop(self):
        if self._hwnd:
            try:
                win32gui.DestroyWindow(self._hwnd)
            except Exception:
                pass