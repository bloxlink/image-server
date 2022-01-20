from sanic import Sanic
import os
from constants import SERVER_HOST, SERVER_PORT
import importlib
import logging

try:
    from os import sched_getaffinity
    cpu_count = len(sched_getaffinity(0))
except ImportError:
    from multiprocessing import cpu_count
    cpu_count = cpu_count()


logging.basicConfig()

def register_routes(path=None):
    path = path or ["src/routes"]
    files = os.listdir('/'.join(path))

    for file_or_folder in files:
        if "__" not in file_or_folder:
            if os.path.isdir(f"{'/'.join(path)}/{file_or_folder}"):
                register_routes(path + [f"{file_or_folder}"])
            else:
                proper_path = "/".join(path) + "/" +  file_or_folder
                import_name = proper_path.replace("/", ".").replace(".py", "").replace("src.", "")

                route_module = importlib.import_module(import_name)
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
    app.run(SERVER_HOST, SERVER_PORT, debug=True, workers=cpu_count)
