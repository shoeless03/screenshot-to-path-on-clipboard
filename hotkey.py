from pynput import keyboard


class HotkeyListener:
    def __init__(self, callback):
        self._callback = callback
        self._listener = keyboard.Listener(on_press=self._on_press)
        self._listener.daemon = True

    def _on_press(self, key):
        if key == keyboard.Key.print_screen:
            self._callback()

    def start(self):
        self._listener.start()

    def stop(self):
        self._listener.stop()
