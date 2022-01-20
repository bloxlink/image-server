from sanic.response import text
from constants import DEFAULT_BACKGROUND


class Route:
    PATH = "/card/default"
    METHODS = ("GET", )

    def __init__(self):
        pass

    async def handler(self, request):
        return text(DEFAULT_BACKGROUND)
