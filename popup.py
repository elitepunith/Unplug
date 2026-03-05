import tkinter as tk
import threading


class ReminderPopup:
    """the checklist popup that shows up when you try to shut down."""

    def __init__(self, reminders, timeout=45):
        self.reminders = reminders
        self.timeout = timeout
        self.remaining = timeout
        self.result = None
        self._done = threading.Event()

    def show(self):
        try:
            self._build_window()
            self.root.mainloop()
        except Exception as e:
            print("[popup] something went wrong: %s" % e)
            self.result = "proceed"
        return self.result or "proceed"

    def _build_window(self):
        self.root = tk.Tk()
        self.root.withdraw()
        self.root.title("Unplug — Shutdown Reminder")
        self.root.geometry("480x450")
        self.root.configure(bg="#1a1b26")
        self.root.attributes("-topmost", True)
        self.root.resizable(False, False)
        self.root.protocol("WM_DELETE_WINDOW", self._on_proceed)

        # slap it in the center
        self.root.update_idletasks()
        sw = self.root.winfo_screenwidth()
        sh = self.root.winfo_screenheight()
        x = (sw - 480) // 2
        y = (sh - 450) // 2
        self.root.geometry("480x450+%d+%d" % (x, y))

        # red banner at the top
        banner = tk.Frame(self.root, bg="#db4b4b", height=80)
        banner.pack(fill="x")
        banner.pack_propagate(False)

        tk.Label(
            banner, text="HOLD ON",
            font=("Segoe UI", 15, "bold"),
            bg="#db4b4b", fg="white",
        ).pack(pady=10)

        tk.Label(
            banner, text="did you check everything?",
            font=("Segoe UI", 9),
            bg="#db4b4b", fg="#ffc0c0",
        ).pack()

        # checklist
        checklist_frame = tk.Frame(self.root, bg="#1a1b26", padx=25, pady=12)
        checklist_frame.pack(fill="both", expand=True)

        self.check_vars = []
        for item in self.reminders:
            var = tk.BooleanVar(value=False)
            self.check_vars.append(var)
            tk.Checkbutton(
                checklist_frame,
                text="  " + item,
                variable=var,
                font=("Segoe UI", 10),
                bg="#1a1b26", fg="#a9b1d6",
                selectcolor="#24283b",
                activebackground="#1a1b26",
                activeforeground="#a9b1d6",
                anchor="w",
                command=self._check_toggled,
            ).pack(fill="x", pady=3)

        # countdown timer
        self.timer_lbl = tk.Label(
            self.root,
            text="auto-proceeding in %ds" % self.remaining,
            font=("Segoe UI", 8),
            bg="#1a1b26", fg="#565f89",
        )
        self.timer_lbl.pack()

        # thin progress bar
        self.bar = tk.Canvas(self.root, height=4, bg="#1a1b26", highlightthickness=0)
        self.bar.pack(fill="x", padx=25, pady=8)

        # buttons
        btn_frame = tk.Frame(self.root, bg="#1a1b26", padx=25)
        btn_frame.pack(fill="x", pady=15)

        self.go_btn = tk.Button(
            btn_frame, text="All good, shut down",
            font=("Segoe UI", 10, "bold"),
            bg="#9ece6a", fg="#1a1b26",
            activebackground="#73b830",
            relief="flat", cursor="hand2",
            command=self._on_proceed,
        )
        self.go_btn.pack(fill="x", ipady=5, pady=3)

        self.cancel_btn = tk.Button(
            btn_frame, text="Wait, go back",
            font=("Segoe UI", 9),
            bg="#db4b4b", fg="white",
            activebackground="#b83030",
            relief="flat", cursor="hand2",
            command=self._on_cancel,
        )
        self.cancel_btn.pack(fill="x", ipady=3, pady=3)

        self.root.deiconify()
        self.root.lift()
        self.root.focus_force()
        self.root.after(100, self._grab_focus)
        self._tick()

    def _grab_focus(self):
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
            self.timer_lbl.config(text="auto-proceeding in %ds" % self.remaining)
            self.bar.delete("all")
            w = self.bar.winfo_width()
            if w > 1:
                frac = self.remaining / self.timeout
                bw = int(w * frac)
                color = "#9ece6a" if self.remaining > 10 else "#db4b4b"
                self.bar.create_rectangle(0, 0, bw, 4, fill=color, outline="")
            self.remaining -= 1
            self.root.after(1000, self._tick)
        except Exception:
            pass

    def _check_toggled(self):
        if all(v.get() for v in self.check_vars):
            self.go_btn.config(bg="#41a832", fg="white", text="All done! Shut down")

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