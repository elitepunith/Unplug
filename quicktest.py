import tkinter as tk

root = tk.Tk()
root.title("Quick Test")
root.geometry("400x300")
root.configure(bg="#1a1b26")

tk.Label(
    root,
    text="IF YOU CAN SEE THIS",
    font=("Segoe UI", 20, "bold"),
    bg="#1a1b26", fg="white",
).pack(pady=30)

tk.Label(
    root,
    text="tkinter is working fine",
    font=("Segoe UI", 12),
    bg="#1a1b26", fg="#9ece6a",
).pack()

tk.Button(
    root,
    text="Close",
    font=("Segoe UI", 12),
    command=root.destroy,
).pack(pady=30)

root.mainloop()
print("window closed, everything works")