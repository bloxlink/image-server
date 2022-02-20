from sanic.response import raw
from PIL import Image, ImageFont, ImageDraw
from io import BytesIO
from config import DEFAULT_VERIFY_BACKGROUND
from IMAGES import IMAGE_CONFIG
import aiohttp


class Route:
    PATH = "/verify/front"
    METHODS = ("GET", )

    def __init__(self):
        self.header1 = ImageFont.truetype("fonts/TovariSans.ttf", 100)
        self.header2 = ImageFont.truetype("fonts/TovariSans.ttf", 50)
       # self.header3 = ImageFont.truetype("fonts/cartoonist/TovariSans.ttf", 90)
        self.header4 = ImageFont.truetype("fonts/TovariSans.ttf", 40)
        self.header5 = ImageFont.truetype("fonts/TovariSans.ttf", 30)

        self.session = None

    async def handler(self, request):
        json_data = request.json
        background   = json_data.get("background")
        background   = background if background and IMAGE_CONFIG.get(background, {}).get("paths", {}).get("verify", {}).get("front") else DEFAULT_VERIFY_BACKGROUND

        username     = json_data.get("username")
        display_name = json_data.get("display_name")
        headshot     = json_data.get("headshot")
        nickname     = json_data.get("nickname")
        roles        = json_data.get("roles")

        background_config = IMAGE_CONFIG[background]
        background_path = background_config["paths"]["verify"]["front"]
        background_props = background_config.get("props", ("bigger_moon.png", "HEADSHOT", "BACKGROUND", "bigger_moon_outline.png"))
        background_hexes = background_config.get("hexes", {})

        primary_color = background_hexes.get("primary_color", (240, 191, 60))

        # image storage for closing
        headshot_image = None

        # buffer storage
        headshot_buffer = None

        if not self.session:
            self.session = aiohttp.ClientSession()

        first_font_size = self.header1
        second_font_size = self.header2

        adjusted_name_pos_1 = 290
        adjusted_name_pos_2 = 370

        if len(username) >= 20:
            username = f"{username[:20]}..."

        if len(display_name) >= 20:
            display_name = f"{display_name[:20]}..."

        if len(username) >= 10 or len(display_name) >= 10:
            first_font_size = self.header2
            second_font_size = self.header2
            adjusted_name_pos_1 = 320
            adjusted_name_pos_2 = 370

        with Image.open(background_path) as background_image:
            image = Image.new("RGBA", (background_image.width, background_image.height))

            for prop in background_props:
                if isinstance(prop, tuple):
                    prop_name = prop[0]
                    prop_dim = prop[1]
                else:
                    prop_name = prop
                    prop_dim = (90, 50) if prop_name == "HEADSHOT" else (0, 0)

                if prop_name == "BACKGROUND":
                    image.paste(background_image, prop_dim, background_image)
                elif prop_name == "HEADSHOT":
                    if headshot:
                        async with self.session.get(headshot) as resp:
                            headshot_buffer = BytesIO(await resp.read())

                            headshot_image  = Image.open(headshot_buffer)
                            headshot_image  = headshot_image.resize((250, 250))
                            image.paste(headshot_image, prop_dim, headshot_image)
                else:
                    with Image.open(f"./assets/props/{prop_name}") as prop_image:
                        image.paste(prop_image, prop_dim, prop_image)

            # if overlay:
            #     with Image.open(f"./assets/props/overlays/{overlay}.png") as overlay_image:
            #         image.paste(overlay_image, (0, 0), overlay_image)

            draw = ImageDraw.Draw(image)

            if username:
                username = f"@{username}"

                if display_name:
                    if username[1:] == display_name:
                        # header is username. don't display display_name
                        width_username = draw.textsize(username, font=first_font_size)[0]

                        draw.text(
                            ((image.size[0]-width_username) * 0.160, adjusted_name_pos_1),
                            username,
                            primary_color,
                            font=first_font_size
                        )
                    else:
                        # show both username and display name
                        width_display_name  = draw.textsize(display_name, font=first_font_size)[0]
                        draw.text(
                            ((image.size[0]-width_display_name) * 0.160, adjusted_name_pos_1),
                            display_name,
                            primary_color,
                            font=first_font_size)

                        width_username = draw.textsize(username, font=second_font_size)[0]
                        draw.text(
                            ((image.size[0]-width_username) * 0.160, adjusted_name_pos_2),
                            username,
                            (255, 255, 255),
                            font=second_font_size)

                else:
                    width_username = draw.textsize(username, font=first_font_size)[0]

                    draw.text(
                        ((image.size[0]-width_username) * 0.160, adjusted_name_pos_1),
                        username,
                        primary_color,
                        font=first_font_size
                    )

            if nickname:
                draw.text(
                    (440, 10),
                    "Nickname: ",
                    primary_color,
                    font=self.header2
                )

                draw.text(
                    (620, 10),
                    f"{nickname}",
                    primary_color,
                    font=self.header4
                )


        try:
            with BytesIO() as bf:
                image.save(bf, "PNG", quality=70)
                image.seek(0)

                return raw(bf.getvalue())

        finally:
            if headshot_buffer:
                headshot_buffer.close()

            if image:
                image.close()

            if headshot_image:
                headshot_image.close()
