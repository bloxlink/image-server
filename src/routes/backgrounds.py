from sanic.response import json
from os import listdir
from constants import IMAGE_CONFIG
import logging


class Route:
    PATH = "/backgrounds"
    METHODS = ("GET", )

    def __init__(self):
        # parse for valid backgrounds
        backgrounds = listdir("./assets/backgrounds/")

        for background in [x for x in backgrounds if not x.startswith("__")]:
            image_config = IMAGE_CONFIG.get(background)

            if not image_config:
                logging.warning(f"No background config found: {background}")

                continue

            image_config["path"] = f"assets/backgrounds/{background}"

        for background_name, background_data in dict(IMAGE_CONFIG).items():
            if not background_data.get("path"):
                logging.warning(f"No background image found for config: {background_name}")

                del IMAGE_CONFIG[background_name]

        self.background_json = json(IMAGE_CONFIG)


    async def handler(self, request):
        # http://localhost:8000/assets/backgrounds/stary_night.jpg

        return self.background_json
