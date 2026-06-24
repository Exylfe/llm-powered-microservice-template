from application.services.phone_controller import PhoneController

class PhoneService:
    """
    Service layer between API and PhoneController.
    Keeps business logic separate from raw ADB execution.
    """

    def __init__(self):
        self.phone = PhoneController()

    def home(self):
        return self.phone.home()

    def back(self):
        return self.phone.back()

    def power(self):
        return self.phone.power()

    def tap(self, x: int, y: int):
        return self.phone.tap(x, y)

    def swipe(self, x1: int, y1: int, x2: int, y2: int, duration: int = 300):
        return self.phone.swipe(x1, y1, x2, y2, duration)

    def text(self, value: str):
        return self.phone.text(value)