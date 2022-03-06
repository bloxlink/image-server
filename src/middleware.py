from sanic.response import text
from config import AUTH


async def auth(request):
    # allow images
    if request.path.endswith(".png") or request.path.endswith(".jpg") or request.path.endswith(".jpeg"):
        return None

    if request.headers.get("Authorization") != AUTH:
        return text("Unauthorized", status=401)
