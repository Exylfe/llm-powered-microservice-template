import subprocess

class PhoneController:
    """
    A simple ADB-based phone control layer.
    This wraps raw adb commands into reusable functions.
    """

    def _run(self, command: str):
        result = subprocess.run(command, shell=True, capture_output=True, text=True)
        return result.stdout.strip()

    # Basic controls
    def home(self):
        return self._run("adb shell input keyevent 3")

    def back(self):
        return self._run("adb shell input keyevent 4")

    def power(self):
        return self._run("adb shell input keyevent 26")

    # Touch control
    def tap(self, x: int, y: int):
        return self._run(f"adb shell input tap {x} {y}")

    def swipe(self, x1: int, y1: int, x2: int, y2: int, duration: int = 300):
        return self._run(f"adb shell input swipe {x1} {y1} {x2} {y2} {duration}")

    # Text input
    def text(self, value: str):
        safe = value.replace(" ", "%s")
        return self._run(f"adb shell input text \"{safe}\"")