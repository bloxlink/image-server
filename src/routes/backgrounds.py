from sanic.response import json
from constants import IMAGE_CONFIG


class Route:
    PATH = "/backgrounds"
    METHODS = ("GET", )

    def __init__(self):
        for background_name, background_data in dict(IMAGE_CONFIG).items():
            if background_data.get("free"):
                background_data["path"] = f"assets/backgrounds/whole/free/{background_name}.png"
                background_data["front"] = f"assets/backgrounds/front/free/{background_name}.png"
                background_data["back"] = f"assets/backgrounds/back/free/{background_name}.png"
            else:
                background_data["path"] = f"assets/backgrounds/whole/{background_name}.png"
                background_data["front"] = f"assets/backgrounds/front/{background_name}.png"
                background_data["back"] = f"assets/backgrounds/back/{background_name}.png"

        self.background_json = json(IMAGE_CONFIG)


    async def handler(self, request):
        return self.background_json
