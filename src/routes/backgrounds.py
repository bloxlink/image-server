from sanic.response import json
from IMAGES import IMAGE_CONFIG
import os



class Route:
    PATH = "/backgrounds"
    METHODS = ("GET", )

    def __init__(self):
        self.getinfo_json = {}
        self.verify_json  = {}

        for background_name, background_data in IMAGE_CONFIG.items():
            if background_data["paths"].get("getinfo"):
                self.getinfo_json[background_name] = background_data

            if background_data["paths"].get("verify"):
                 self.verify_json[background_name] = background_data

        self.background_json = json(IMAGE_CONFIG)
        self.getinfo_json = json(self.getinfo_json)
        self.verify_json = json(self.verify_json)


    async def handler(self, request):
        typex = request.args.get("type")

        if typex == "getinfo":
            return self.getinfo_json
        elif typex == "verify":
            return self.verify_json

        return self.background_json
