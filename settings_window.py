import tkinter as tk
from tkinter import filedialog

import config


def show(root):
    cfg = config.load()

    win = tk.Toplevel(root)
    win.title("Screenshot Tool - Settings")
    win.resizable(False, False)
    win.attributes("-topmost", True)

    frame = tk.Frame(win, padx=15, pady=15)
    frame.pack(fill=tk.BOTH, expand=True)

    # Save directory
    tk.Label(frame, text="Save Directory:", anchor="w").pack(fill=tk.X)

    dir_frame = tk.Frame(frame)
    dir_frame.pack(fill=tk.X, pady=(2, 10))

    dir_var = tk.StringVar(value=cfg["save_dir"])
    tk.Entry(dir_frame, textvariable=dir_var, width=45).pack(side=tk.LEFT, fill=tk.X, expand=True)

    def browse_dir():
        path = filedialog.askdirectory(initialdir=dir_var.get())
        if path:
            dir_var.set(path)

    tk.Button(dir_frame, text="Browse...", command=browse_dir).pack(side=tk.LEFT, padx=(5, 0))

    # Tray icon
    tk.Label(frame, text="Tray Icon (PNG/ICO, leave empty for default):", anchor="w").pack(fill=tk.X)

    icon_frame = tk.Frame(frame)
    icon_frame.pack(fill=tk.X, pady=(2, 10))

    icon_var = tk.StringVar(value=cfg.get("icon_path", ""))
    tk.Entry(icon_frame, textvariable=icon_var, width=45).pack(side=tk.LEFT, fill=tk.X, expand=True)

    def browse_icon():
        path = filedialog.askopenfilename(
            filetypes=[("Image files", "*.png *.ico *.jpg *.bmp"), ("All files", "*.*")]
        )
        if path:
            icon_var.set(path)

    tk.Button(icon_frame, text="Browse...", command=browse_icon).pack(side=tk.LEFT, padx=(5, 0))

    # Copy mode
    tk.Label(frame, text="Copy to Clipboard:", anchor="w").pack(fill=tk.X)

    copy_frame = tk.Frame(frame)
    copy_frame.pack(fill=tk.X, pady=(2, 10))

    copy_var = tk.StringVar(value=cfg.get("copy_mode", "path"))
    tk.Radiobutton(copy_frame, text="File path", variable=copy_var, value="path").pack(side=tk.LEFT, padx=(0, 15))
    tk.Radiobutton(copy_frame, text="Image", variable=copy_var, value="image").pack(side=tk.LEFT)

    def on_save():
        cfg["save_dir"] = dir_var.get()
        cfg["icon_path"] = icon_var.get()
        cfg["copy_mode"] = copy_var.get()
        config.save(cfg)
        win.destroy()

    btn_frame = tk.Frame(frame)
    btn_frame.pack(fill=tk.X, pady=(0, 10))
    tk.Button(btn_frame, text="Save", command=on_save, width=10).pack(side=tk.RIGHT, padx=(5, 0))
    tk.Button(btn_frame, text="Cancel", command=win.destroy, width=10).pack(side=tk.RIGHT)

    sep = tk.Frame(frame, height=1, bg="gray")
    sep.pack(fill=tk.X, pady=(0, 8))

    tk.Label(
        frame,
        text=f"Screenshot Tool v{config.VERSION}",
        fg="gray",
        anchor="w",
        font=("Segoe UI", 8),
    ).pack(fill=tk.X)

    win.update_idletasks()
    w = win.winfo_width()
    h = win.winfo_height()
    x = (win.winfo_screenwidth() // 2) - (w // 2)
    y = (win.winfo_screenheight() // 2) - (h // 2)
    win.geometry(f"+{x}+{y}")
