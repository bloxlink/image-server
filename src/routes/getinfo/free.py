from sanic.response import raw
from PIL import Image, ImageColor
from io import BytesIO


class Route:
    PATH = "/getinfo/free"
    METHODS = ("GET", )

    def __init__(self):
        pass

    async def handler(self, request):
        color = f"#{request.args.get('color')}"

        with Image.open(f"./assets/props/free_card.png") as prop_image:
            with Image.new("RGB", (prop_image.width, prop_image.height), ImageColor.getrgb(color)) as image:
                image.paste(prop_image, (0, 0), prop_image)

                with BytesIO() as bf:
                    image.save(bf, "PNG", quality=70)
                    image.seek(0)

                    return raw(bf.getvalue())
