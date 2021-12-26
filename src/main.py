from sanic import Sanic
from os import listdir
import importlib

def register_routes():
    routes = listdir("routes/")

    for route_name in [x.replace(".py", "") for x in routes if not x.startswith("__")]:
        route_module = importlib.import_module(f"routes.{route_name}")

        route = getattr(route_module, "Route")()
        app.add_route(
            getattr(route, "handler"),
            getattr(route, "PATH"),
            getattr(route, "METHODS")
        )



if __name__ == '__main__':
    app = Sanic("ImageServer")

    app.static('/assets', "./assets")


    register_routes()
    app.run(port=8000, debug=True)

