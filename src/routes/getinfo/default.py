from sanic.response import text
from config import DEFAULT_GETINFO_BACKGROUND, DEFAULT_VERIFY_BACKGROUND


class Route:
    PATH = "/getinfo/default"
    METHODS = ("GET", )

    def __init__(self):
        pass

    async def handler(self, request):
        type = request.args.get("type")

        if type == "getinfo":
            return text(DEFAULT_GETINFO_BACKGROUND)
        elif type == "verify":
            return text(DEFAULT_VERIFY_BACKGROUND)
