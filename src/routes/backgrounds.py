from tkinter.tix import IMAGE
from turtle import back
from sanic.response import json
from IMAGES import IMAGE_CONFIG
import os



class Route:
    PATH = "/backgrounds"
    METHODS = ("GET", )

    def __init__(self):
        self.background_json = json(IMAGE_CONFIG)


    async def handler(self, request):
        return self.background_json
