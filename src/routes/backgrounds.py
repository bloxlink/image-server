from sanic.response import json
from os import listdir
from constants import IMAGE_CONFIG


class Route:
    PATH = "/backgrounds"
    METHODS = ("GET", )

    def __init__(self):
        pass

    async def handler(self, request):
        # http://localhost:8000/assets/backgrounds/stary_night.jpg


        return json({

        })
