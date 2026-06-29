import json
import sys
from pathlib import Path

VERSION = "1.0.0"

_CONFIG_DIR = Path.home() / ".screenshot-tool"
_CONFIG_FILE = _CONFIG_DIR / "config.json"

_DEFAULTS = {
    "save_dir": None,
    "icon_path": "",
}


def _default_save_dir():
    if sys.platform == "win32":
        return str(Path.home() / "Pictures" / "Screenshots")
    return str(Path.home() / "Pictures")


def load():
    cfg = {"save_dir": _default_save_dir(), "icon_path": "", "copy_mode": "path"}
    if _CONFIG_FILE.exists():
        try:
            data = json.loads(_CONFIG_FILE.read_text())
            save_dir = data.get("save_dir")
            if isinstance(save_dir, str) and save_dir.strip():
                cfg["save_dir"] = save_dir
            icon_path = data.get("icon_path", "")
            if isinstance(icon_path, str):
                cfg["icon_path"] = icon_path
            copy_mode = data.get("copy_mode", "path")
            if copy_mode in ("path", "image"):
                cfg["copy_mode"] = copy_mode
        except (json.JSONDecodeError, KeyError):
            pass
    return cfg


def save(cfg):
    _CONFIG_DIR.mkdir(parents=True, exist_ok=True)
    _CONFIG_FILE.write_text(json.dumps(cfg, indent=2))
