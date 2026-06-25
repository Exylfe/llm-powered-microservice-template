from application.services.phone_service import PhoneService

class ToolRegistry:
    """
    Maps AI tool names → actual system actions.
    """

    def __init__(self):
        self.phone = PhoneService()

    def execute(self, tool_name: str, params: dict):
        if tool_name == "phone_home":
            return self.phone.home()

        if tool_name == "phone_back":
            return self.phone.back()

        if tool_name == "phone_power":
            return self.phone.power()

        if tool_name == "phone_tap":
            return self.phone.tap(params["x"], params["y"])

        if tool_name == "phone_swipe":
            return self.phone.swipe(
                params["x1"], params["y1"],
                params["x2"], params["y2"],
                params.get("duration", 300)
            )

        if tool_name == "phone_text":
            return self.phone.text(params["text"])

        raise ValueError(f"Unknown tool: {tool_name}")