from os import environ as env

SERVER_HOST = "0.0.0.0"
SERVER_PORT = 8000
AUTH = env.get("IMAGE_SERVER_AUTH", "oof")

DEFAULT_GETINFO_BACKGROUND = "breezy_meadows"
DEFAULT_VERIFY_BACKGROUND = "breezy_meadows"
