import io
import sys


def copy_path(text):
    if sys.platform == "win32":
        import subprocess
        subprocess.Popen(["clip"], stdin=subprocess.PIPE, shell=True).communicate(text.encode("utf-16-le"))
    else:
        try:
            import pyperclip
            pyperclip.copy(text)
        except Exception:
            pass


def copy_image(image):
    if sys.platform == "win32":
        import ctypes

        buf = io.BytesIO()
        image.convert("RGB").save(buf, "BMP")
        bmp_data = buf.getvalue()[14:]

        user32 = ctypes.windll.user32
        kernel32 = ctypes.windll.kernel32

        kernel32.GlobalAlloc.restype = ctypes.c_void_p
        kernel32.GlobalLock.restype = ctypes.c_void_p
        kernel32.GlobalLock.argtypes = [ctypes.c_void_p]
        kernel32.GlobalUnlock.argtypes = [ctypes.c_void_p]
        user32.SetClipboardData.argtypes = [ctypes.c_uint, ctypes.c_void_p]

        CF_DIB = 8
        GMEM_MOVEABLE = 0x0002

        h = kernel32.GlobalAlloc(GMEM_MOVEABLE, len(bmp_data))
        p = kernel32.GlobalLock(h)
        ctypes.memmove(p, bmp_data, len(bmp_data))
        kernel32.GlobalUnlock(h)

        user32.OpenClipboard(0)
        user32.EmptyClipboard()
        user32.SetClipboardData(CF_DIB, h)
        user32.CloseClipboard()
    else:
        try:
            import subprocess
            buf = io.BytesIO()
            image.save(buf, "PNG")
            subprocess.Popen(
                ["xclip", "-selection", "clipboard", "-t", "image/png"],
                stdin=subprocess.PIPE,
            ).communicate(buf.getvalue())
        except Exception:
            pass
