from sanic.response import json
from os import listdir
from constants import IMAGE_CONFIG
import logging


class Route:
    PATH = "/backgrounds"
    METHODS = ("GET", )

    def __init__(self):
        # parse for valid backgrounds
        front_cards = set(x.replace(".png", "") for x in listdir("./assets/backgrounds/front/") if not x.startswith("__"))
        back_cards  = set(x.replace(".png", "") for x in listdir("./assets/backgrounds/back/") if not x.startswith("__"))
        whole_cards = set(x.replace(".jpg", "") for x in listdir("./assets/backgrounds/whole/") if not x.startswith("__"))

        valid_cards = front_cards.intersection(back_cards).intersection(whole_cards)
        invalid_cards = front_cards.difference(back_cards).union(back_cards.difference(front_cards)).difference(whole_cards)

        if invalid_cards:
            map(lambda b: logging.error(f"Invalid background: {b}"), invalid_cards)

        for background in valid_cards:
            image_config = IMAGE_CONFIG.get(background)

            if image_config:
                image_config["front"] = f"assets/backgrounds/front/{background}.png"
                image_config["back"] = f"assets/backgrounds/back/{background}.png"
                image_config["whole"] = f"assets/backgrounds/whole/{background}.jpg"
            else:
                logging.error(f"No image config for {background}")

        for background_name, background_data in dict(IMAGE_CONFIG).items():
            if not background_data.get("whole"):
                logging.error(f"Missing front or back for background image: {background_name}")

                del IMAGE_CONFIG[background_name]

        self.background_json = json(IMAGE_CONFIG)


    async def handler(self, request):
        # http://localhost:8000/assets/backgrounds/stary_night.jpg

        return self.background_json
