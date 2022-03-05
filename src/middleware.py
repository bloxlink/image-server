from sanic.response import text
from config import AUTH


async def auth(request):
    if request.headers.get("Authorization") != AUTH:
        return text("Unauthorized", status=401)
