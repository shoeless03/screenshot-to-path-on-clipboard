import ctypes
import os
import sys
import tkinter as tk

if sys.platform == "win32":
    ctypes.windll.shcore.SetProcessDpiAwareness(2)

import capture
import clipboard
import overlay
import settings_window
import storage
from hotkey import HotkeyListener
from tray import create_tray

_capturing = False


def take_screenshot(root):
    global _capturing
    if _capturing:
        return
    _capturing = True

    screen = capture.grab_screen()
    region = overlay.select_region(root, screen)
    _capturing = False
    if region is None:
        return
    cropped = capture.crop(screen, region)
    path = storage.save(cropped)
    clipboard.copy(path)


def main():
    root = tk.Tk()
    root.withdraw()

    def on_hotkey():
        root.after(0, lambda: take_screenshot(root))

    def on_settings():
        root.after(0, lambda: settings_window.show(root))

    def on_restart():
        listener.stop()
        icon.stop()
        root.after(0, root.destroy)
        os.execv(sys.executable, [sys.executable] + sys.argv)

    def on_quit():
        listener.stop()
        icon.stop()
        root.after(0, root.destroy)

    listener = HotkeyListener(on_hotkey)
    listener.start()

    icon = create_tray(on_settings=on_settings, on_restart=on_restart, on_quit=on_quit)
    icon.run_detached()

    root.mainloop()


if __name__ == "__main__":
    main()
