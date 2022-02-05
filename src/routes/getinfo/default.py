from sanic.response import text
from config import DEFAULT_BACKGROUND


class Route:
    PATH = "/getinfo/default"
    METHODS = ("GET", )

    def __init__(self):
        pass

    async def handler(self, request):
        return text(DEFAULT_BACKGROUND)
