from sanic.response import raw
from PIL import Image, ImageFont, ImageDraw
from io import BytesIO
from utils.text_cleanse import cleanse
from config import DEFAULT_GETINFO_BACKGROUND
from IMAGES import IMAGE_CONFIG


class Route:
    PATH = "/getinfo/back"
    METHODS = ("GET", )

    def __init__(self):
        self.header1 = ImageFont.truetype("fonts/TovariSans.ttf", 100)
        self.header2 = ImageFont.truetype("fonts/TovariSans.ttf", 50)
        self.header3 = ImageFont.truetype("fonts/TovariSans.ttf", 40)
        self.header4 = ImageFont.truetype("fonts/TovariSans.ttf", 30)

    async def handler(self, request):
        json_data = request.json
        background   = json_data.get("background")
        background   = background if background and IMAGE_CONFIG.get(background, {}).get("paths", {}).get("getinfo", {}).get("back") else DEFAULT_GETINFO_BACKGROUND

        banned          = json_data.get("banned") == "true"
        username        = json_data.get("username")
        display_name    = json_data.get("display_name")
        group_ranks     =  json_data.get("group_ranks", {})
        selected_ranks  = {k: group_ranks[k] for k in list(group_ranks)[:5]}

        if banned:
            background = "black"

        background_config = IMAGE_CONFIG[background]
        background_path = background_config["paths"]["getinfo"]["back"]
        background_hexes = background_config.get("hexes", {})

        primary_color = background_hexes.get("primary_color", (240, 191, 60))

        first_font_size = self.header1
        second_font_size = self.header2

        adjusted_name_pos_1 = 30
        adjusted_name_pos_2 = 110

        if len(username) >= 20:
            username = f"{username[:20]}..."

        if len(display_name) >= 20:
            display_name = f"{display_name[:20]}..."

        if len(username) >= 20 or len(display_name) >= 20:
            first_font_size = self.header3
            second_font_size = self.header3
            adjusted_name_pos_1 = 100
            adjusted_name_pos_2 = 140

        elif len(username) >= 10 or len(display_name) >= 10:
            first_font_size = self.header2
            second_font_size = self.header2
            adjusted_name_pos_1 = 80
            adjusted_name_pos_2 = 130

        with Image.open(background_path) as image:
            draw = ImageDraw.Draw(image)

            if username:
                username = f"@{username}"

                if display_name:
                    if username[1:] == display_name:
                        # header is username. don't display display_name
                        width_username = draw.textsize(username, font=first_font_size)[0]

                        draw.text(
                            ((image.size[0]-width_username) / 2, 100),
                            username,
                            (255, 255, 255),
                            font=first_font_size
                        )
                    else:
                        # show both username and display name
                        width_display_name  = draw.textsize(display_name, font=first_font_size)[0]
                        draw.text(
                            ((image.size[0]-width_display_name) / 2, adjusted_name_pos_1),
                            display_name,
                            primary_color,
                            font=first_font_size)

                        width_username = draw.textsize(username, font=second_font_size)[0]
                        draw.text(
                            ((image.size[0]-width_username) / 2, adjusted_name_pos_2),
                            username,
                            (255, 255, 255),
                            font=second_font_size)

                else:
                    width_username = draw.textsize(username, font=first_font_size)[0]

                    draw.text(
                        ((image.size[0]-width_username) / 2, 30),
                        username,
                        (255, 255, 255),
                        font=self.header1
                    )

            if selected_ranks:
                group_name_pos = 265
                group_rank_pos = 300

                for group_name, group_rank in selected_ranks.items():
                    draw.text(
                        (50, group_name_pos),
                        group_name,
                        (255, 255, 255),
                        font=self.header3
                    )
                    draw.text(
                        (50, group_rank_pos),
                        group_rank,
                        (255, 71, 71),
                        font=self.header3
                    )

                    group_name_pos += 80
                    group_rank_pos += 80


            with BytesIO() as bf:
                image.save(bf, "PNG", quality=70)
                image.seek(0)

                return raw(bf.getvalue())
