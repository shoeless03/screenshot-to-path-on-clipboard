from pathlib import Path

import pystray
from PIL import Image

import config

_DEFAULT_ICON = Path(__file__).parent / "555555.PNG"


def _load_icon_image():
    cfg = config.load()
    icon_path = cfg.get("icon_path", "")
    if icon_path and Path(icon_path).is_file():
        try:
            img = Image.open(icon_path)
            img = img.resize((64, 64), Image.LANCZOS)
            return img
        except Exception:
            pass
    if _DEFAULT_ICON.is_file():
        try:
            img = Image.open(_DEFAULT_ICON)
            img = img.resize((64, 64), Image.LANCZOS)
            return img
        except Exception:
            pass
    return Image.new("RGB", (64, 64), (70, 130, 180))


def create_tray(on_settings, on_restart, on_quit):
    icon = pystray.Icon(
        "screenshot",
        _load_icon_image(),
        "Screenshot Tool",
        menu=pystray.Menu(
            pystray.MenuItem("Settings", lambda: on_settings()),
            pystray.MenuItem("Restart", lambda: on_restart()),
            pystray.Menu.SEPARATOR,
            pystray.MenuItem("Quit", lambda: on_quit()),
        ),
    )
    return icon
