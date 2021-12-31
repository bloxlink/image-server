from sanic import Sanic
from os import listdir
from constants import SERVER_HOST, SERVER_PORT
import importlib
import logging

logging.basicConfig()

def register_routes():
    routes = listdir("src/routes/")

    for route_name in [x.replace(".py", "") for x in routes if not x.startswith("__")]:
        route_module = importlib.import_module(f"routes.{route_name}")

        route = getattr(route_module, "Route")()
        app.add_route(
            getattr(route, "handler"),
            getattr(route, "PATH"),
            getattr(route, "METHODS")
        )



if __name__ == '__main__':
    app = Sanic("BloxlinkImageServer")

    app.static("/assets", "./assets")


    register_routes()
    app.run(SERVER_HOST, SERVER_PORT, debug=True)
