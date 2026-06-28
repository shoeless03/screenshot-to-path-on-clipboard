import sys


def copy(text):
    if sys.platform == "win32":
        import subprocess
        subprocess.Popen(["clip"], stdin=subprocess.PIPE, shell=True).communicate(text.encode("utf-16-le"))
    else:
        try:
            import pyperclip
            pyperclip.copy(text)
        except Exception:
            pass
