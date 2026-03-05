import time
import subprocess
import logging

try:
    import win32gui
    import win32con
    import win32api
    HAS_WIN32 = True
except ImportError:
    HAS_WIN32 = False


logger = logging.getLogger("shutdown_reminder")


class ShutdownListener:
    """
    creates a hidden window that receives windows messages.
    when windows sends WM_QUERYENDSESSION (meaning "hey im about
    to shut down, you cool with that?"), we intercept it,
    show the popup, and either allow or block it.

    this is the standard win32 way to do it and it works
    on windows 7 just fine.
    """

    def __init__(self, on_shutdown_detected):
        """
        on_shutdown_detected: callable that returns True to allow
                              shutdown, False to block it
        """
        if not HAS_WIN32:
            raise RuntimeError(
                "pywin32 is required. run: pip install pywin32"
            )

        self.on_shutdown_detected = on_shutdown_detected
        self._hwnd = None
        self._class_atom = None

    def start(self):
        """register the hidden window and start pumping messages"""
        logger.info("registering shutdown listener window")

        wc = win32gui.WNDCLASS()
        wc.lpfnWndProc = self._wnd_proc
        wc.lpszClassName = "ShutdownReminderHiddenWnd"
        wc.hInstance = win32api.GetModuleHandle(None)

        self._class_atom = win32gui.RegisterClass(wc)
        self._hwnd = win32gui.CreateWindow(
            self._class_atom,
            "ShutdownReminderHidden",
            0,      # style (invisible)
            0, 0,   # position
            0, 0,   # size
            0,      # parent
            0,      # menu
            wc.hInstance,
            None,
        )

        logger.info("hidden window created (hwnd={})".format(self._hwnd))
        self._pump_messages()

    def _wnd_proc(self, hwnd, msg, wparam, lparam):
        if msg == win32con.WM_QUERYENDSESSION:
            logger.info("WM_QUERYENDSESSION received")
            try:
                allow = self.on_shutdown_detected()
            except Exception as e:
                logger.error("popup callback failed: {}".format(e))
                allow = True  # dont trap the user if we crash

            if allow:
                logger.info("user said proceed, allowing shutdown")
                return True
            else:
                logger.info("user said cancel, blocking shutdown")
                self._cancel_shutdown()
                return False

        if msg == win32con.WM_ENDSESSION:
            logger.info("WM_ENDSESSION received, shutdown is happening")
            return 0

        if msg == win32con.WM_DESTROY:
            win32gui.PostQuitMessage(0)
            return 0

        return win32gui.DefWindowProc(hwnd, msg, wparam, lparam)

    def _pump_messages(self):
        """
        message loop. this is blocking. win32gui.PumpMessages() would also
        work but this gives us a chance to handle KeyboardInterrupt.
        """
        logger.info("message pump started")
        try:
            while True:
                win32gui.PumpWaitingMessages()
                time.sleep(0.1)
        except KeyboardInterrupt:
            logger.info("stopped by ctrl+c")
            self.stop()

    def _cancel_shutdown(self):
        """try to abort a pending shutdown"""
        try:
            result = subprocess.run(
                ["shutdown", "/a"],
                capture_output=True,
                timeout=5,
            )
            if result.returncode == 0:
                logger.info("shutdown cancelled successfully")
            else:
                logger.warning(
                    "shutdown /a returned code {}".format(result.returncode)
                )
        except subprocess.TimeoutExpired:
            logger.warning("shutdown /a timed out")
        except FileNotFoundError:
            logger.error("shutdown command not found (weird)")
        except Exception as e:
            logger.error("failed to cancel shutdown: {}".format(e))

    def stop(self):
        if self._hwnd:
            try:
                win32gui.DestroyWindow(self._hwnd)
            except Exception:
                pass