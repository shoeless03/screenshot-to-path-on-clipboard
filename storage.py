from datetime import datetime
from pathlib import Path

import config


def save(image):
    cfg = config.load()
    d = Path(cfg["save_dir"])
    d.mkdir(parents=True, exist_ok=True)
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S_%f")
    path = d / f"screenshot_{timestamp}.png"
    image.save(str(path))
    return str(path)
