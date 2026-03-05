import tkinter as tk
import threading


class ReminderPopup:
    """
    the main popup that shows up when shutdown is detected.
    shows a checklist of reminders, a countdown, and two buttons.
    user can either acknowledge and let shutdown happen, or cancel it.
    """

    def __init__(self, reminders, timeout=45):
        self.reminders = reminders
        self.timeout = timeout
        self.remaining = timeout
        self.result = None
        self._done = threading.Event()

    def show(self):
        """
        blocks until user makes a choice or timer runs out.
        returns "proceed" or "cancel".
        """
        try:
            self._build_window()
            self.root.mainloop()
        except Exception as e:
            print("[popup] crashed: {}".format(e))
            self.result = "proceed"
        return self.result or "proceed"

    def _build_window(self):
        self.root = tk.Tk()
        self.root.withdraw()  # hide first, show after building

        self.root.title("Shutdown Reminder")
        self.root.geometry("480x420")
        self.root.configure(bg="#1a1b26")
        self.root.attributes("-topmost", True)
        self.root.resizable(False, False)
        self.root.protocol("WM_DELETE_WINDOW", self._on_proceed)

        # center it on screen
        self.root.update_idletasks()
        sw = self.root.winfo_screenwidth()
        sh = self.root.winfo_screenheight()
        x = (sw - 480) // 2
        y = (sh - 420) // 2
        self.root.geometry("480x420+{}+{}".format(x, y))

        # -- top banner --
        banner = tk.Frame(self.root, bg="#db4b4b", height=60)
        banner.pack(fill="x")
        banner.pack_propagate(False)

        tk.Label(
            banner,
            text="SHUTDOWN DETECTED",
            font=("Segoe UI", 15, "bold"),
            bg="#db4b4b", fg="white",
        ).pack(pady=(10, 0))

        tk.Label(
            banner,
            text="check these before you go:",
            font=("Segoe UI", 9),
            bg="#db4b4b", fg="#ffc0c0",
        ).pack()

        # -- checklist area --
        checklist_area = tk.Frame(self.root, bg="#1a1b26", padx=25, pady=12)
        checklist_area.pack(fill="both", expand=True)

        self.check_vars = []
        for reminder in self.reminders:
            var = tk.BooleanVar(value=False)
            self.check_vars.append(var)
            cb = tk.Checkbutton(
                checklist_area,
                text="  " + reminder,
                variable=var,
                font=("Segoe UI", 10),
                bg="#1a1b26", fg="#a9b1d6",
                selectcolor="#24283b",
                activebackground="#1a1b26",
                activeforeground="#a9b1d6",
                anchor="w",
                command=self._on_check_changed,
            )
            cb.pack(fill="x", pady=3)

        # -- timer --
        self.timer_label = tk.Label(
            self.root,
            text="auto-proceeding in {}s".format(self.remaining),
            font=("Segoe UI", 8),
            bg="#1a1b26", fg="#565f89",
        )
        self.timer_label.pack()

        # -- progress bar --
        self.progress_canvas = tk.Canvas(
            self.root, height=4, bg="#1a1b26",
            highlightthickness=0,
        )
        self.progress_canvas.pack(fill="x", padx=25, pady=(4, 8))

        # -- buttons --
        btn_area = tk.Frame(self.root, bg="#1a1b26", padx=25, pady=(0, 15))
        btn_area.pack(fill="x")

        self.proceed_btn = tk.Button(
            btn_area,
            text="All good, shut down",
            font=("Segoe UI", 10, "bold"),
            bg="#9ece6a", fg="#1a1b26",
            activebackground="#73b830",
            relief="flat", cursor="hand2",
            command=self._on_proceed,
        )
        self.proceed_btn.pack(fill="x", ipady=5, pady=(0, 6))

        self.cancel_btn = tk.Button(
            btn_area,
            text="Wait, cancel shutdown",
            font=("Segoe UI", 9),
            bg="#db4b4b", fg="white",
            activebackground="#b83030",
            relief="flat", cursor="hand2",
            command=self._on_cancel,
        )
        self.cancel_btn.pack(fill="x", ipady=3)

        # now show the window and force it to the front
        self.root.deiconify()
        self.root.lift()
        self.root.focus_force()
        self.root.after(100, self._force_focus)

        # start countdown
        self._tick()

    def _force_focus(self):
        """hit it again after 100ms to really make sure its on top"""
        try:
            self.root.lift()
            self.root.attributes("-topmost", True)
            self.root.focus_force()
        except Exception:
            pass

    def _tick(self):
        if self.remaining <= 0:
            self._on_proceed()
            return

        try:
            self.timer_label.config(
                text="auto-proceeding in {}s".format(self.remaining)
            )

            # update progress bar
            self.progress_canvas.delete("all")
            w = self.progress_canvas.winfo_width()
            if w > 1:
                fraction = self.remaining / self.timeout
                bar_w = int(w * fraction)
                color = "#9ece6a" if self.remaining > 10 else "#db4b4b"
                self.progress_canvas.create_rectangle(
                    0, 0, bar_w, 4, fill=color, outline=""
                )

            self.remaining -= 1
            self.root.after(1000, self._tick)
        except Exception:
            # window got destroyed mid-tick, thats fine
            pass

    def _on_check_changed(self):
        all_done = all(v.get() for v in self.check_vars)
        if all_done:
            self.proceed_btn.config(
                bg="#41a832", fg="white", text="All checked! Shut down"
            )

    def _on_proceed(self):
        self.result = "proceed"
        self._done.set()
        try:
            self.root.destroy()
        except Exception:
            pass

    def _on_cancel(self):
        self.result = "cancel"
        self._done.set()
        try:
            self.root.destroy()
        except Exception:
            pass