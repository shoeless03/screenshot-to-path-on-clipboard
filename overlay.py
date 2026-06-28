import sys
import tkinter as tk

from PIL import ImageTk, Image


def _get_virtual_screen_bbox():
    if sys.platform == "win32":
        import ctypes
        user32 = ctypes.windll.user32
        left = user32.GetSystemMetrics(76)
        top = user32.GetSystemMetrics(77)
        width = user32.GetSystemMetrics(78)
        height = user32.GetSystemMetrics(79)
        return left, top, width, height
    return None


def select_region(root, screenshot):
    result = {}

    bbox = _get_virtual_screen_bbox()

    win = tk.Toplevel(root)
    win.overrideredirect(True)
    win.attributes("-topmost", True)
    win.configure(cursor="crosshair")

    if bbox:
        virt_left, virt_top, virt_w, virt_h = bbox
        win.geometry(f"{virt_w}x{virt_h}")
        win.update_idletasks()
        win.geometry(f"+{virt_left}+{virt_top}")
    else:
        win.attributes("-fullscreen", True)
        win.update_idletasks()
        virt_w = win.winfo_screenwidth()
        virt_h = win.winfo_screenheight()

    screenshot = screenshot.convert("RGB")
    display_img = screenshot.resize((virt_w, virt_h), Image.LANCZOS)
    darkened = Image.blend(display_img, Image.new("RGB", display_img.size, (0, 0, 0)), 0.3)
    bg_photo = ImageTk.PhotoImage(darkened)

    canvas = tk.Canvas(win, width=virt_w, height=virt_h, highlightthickness=0)
    canvas.pack(fill=tk.BOTH, expand=True)
    canvas.create_image(0, 0, anchor=tk.NW, image=bg_photo)

    state = {"start_x": 0, "start_y": 0, "rect": None, "bright_item": None}

    def on_press(event):
        state["start_x"] = event.x
        state["start_y"] = event.y

    def on_drag(event):
        if state["bright_item"]:
            canvas.delete(state["bright_item"])
        if state["rect"]:
            canvas.delete(state["rect"])

        x1, y1 = state["start_x"], state["start_y"]
        x2, y2 = event.x, event.y

        left, top = min(x1, x2), min(y1, y2)
        right, bottom = max(x1, x2), max(y1, y2)

        if right > left and bottom > top:
            cropped = display_img.crop((left, top, right, bottom))
            state["_bright_ref"] = ImageTk.PhotoImage(cropped)
            state["bright_item"] = canvas.create_image(left, top, anchor=tk.NW, image=state["_bright_ref"])

        state["rect"] = canvas.create_rectangle(x1, y1, x2, y2, outline="white", width=2)

    def on_release(event):
        x1, y1 = state["start_x"], state["start_y"]
        x2, y2 = event.x, event.y
        if abs(x2 - x1) > 5 and abs(y2 - y1) > 5:
            img_w, img_h = screenshot.size
            scale_x = img_w / virt_w
            scale_y = img_h / virt_h
            result["region"] = (
                int(min(x1, x2) * scale_x),
                int(min(y1, y2) * scale_y),
                int(max(x1, x2) * scale_x),
                int(max(y1, y2) * scale_y),
            )
        win.destroy()

    def on_escape(event):
        win.destroy()

    canvas.bind("<ButtonPress-1>", on_press)
    canvas.bind("<B1-Motion>", on_drag)
    canvas.bind("<ButtonRelease-1>", on_release)
    win.bind("<Escape>", on_escape)

    win.grab_set()
    win.wait_window()
    return result.get("region")
