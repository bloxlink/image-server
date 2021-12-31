from sanic.response import raw
from PIL import Image, ImageFont, ImageDraw
from io import BytesIO
from utils.image import gradient_text
import aiohttp



class TextWrapper(object):
    # https://stackoverflow.com/questions/7698231/python-pil-draw-multiline-text-on-image
    """ Helper class to wrap text in lines, based on given text, font
        and max allowed line width.
    """

    def __init__(self, text, font, max_width):
        self.text = text
        self.text_lines = [
            ' '.join([w.strip() for w in l.split(' ') if w])
            for l in text.split('\n')
            if l
        ]
        self.font = font
        self.max_width = max_width

        self.draw = ImageDraw.Draw(
            Image.new(
                mode='RGB',
                size=(100, 100)
            )
        )

        self.space_width = self.draw.textsize(
            text=' ',
            font=self.font
        )[0]

    def get_text_width(self, text):
        return self.draw.textsize(
            text=text,
            font=self.font
        )[0]

    def wrapped_text(self):
        wrapped_lines = []
        buf = []
        buf_width = 0

        for line in self.text_lines:
            for word in line.split(' '):
                word_width = self.get_text_width(word)

                expected_width = word_width if not buf else \
                    buf_width + self.space_width + word_width

                if expected_width <= self.max_width:
                    # word fits in line
                    buf_width = expected_width
                    buf.append(word)
                else:
                    # word doesn't fit in line
                    wrapped_lines.append(' '.join(buf))
                    buf = [word]
                    buf_width = word_width

            if buf:
                wrapped_lines.append(' '.join(buf))
                buf = []
                buf_width = 0

        return '\n'.join(wrapped_lines)


class Route:
    PATH = "/profile"
    METHODS = ("GET", )

    def __init__(self):
        self.header1 = ImageFont.truetype("fonts/TovariSans.ttf", 100)
        self.header2 = ImageFont.truetype("fonts/TovariSans.ttf", 50)
       # self.header3 = ImageFont.truetype("fonts/cartoonist/TovariSans.ttf", 90)
        self.header4 = ImageFont.truetype("fonts/TovariSans.ttf", 40)

        self.session = None

    async def handler(self, request):
        # TODO: take in a ?premium=true value to return background; otherwise, return gradient

        background   = request.args.get("background")
        username     = request.args.get("username")
        display_name = request.args.get("display_name")
        description  = request.args.get("description")
        headshot     = request.args.get("headshot")

        # image storage for closing
        image          = None
        headshot_image = None

        # buffer storage
        headshot_buffer = None

        if not self.session:
            self.session = aiohttp.ClientSession()

        with Image.open(f"./assets/backgrounds/{background}.png") as background_image:
            image = Image.new("RGBA", (background_image.width, background_image.height))

            if headshot:
                async with self.session.get(headshot) as resp:
                    with Image.open("./assets/props/moon.png") as moon_image:
                        with Image.open("./assets/props/moon_outline.png") as moon_outline_image:
                            headshot_buffer = BytesIO(await resp.read())
                            headshot_image  = Image.open(headshot_buffer)
                            headshot_image  = headshot_image.resize((220, 220))

                            image.paste(moon_image, (0, 0), moon_image)
                            image.paste(headshot_image, (160, 70), headshot_image)

                            image.paste(background_image, (0, 0), background_image)
                            image.paste(moon_outline_image, (0, 0), moon_outline_image)


            draw = ImageDraw.Draw(image)

            if username:
                username = f"@{username}"

                if display_name:
                    if username[1:] == display_name:
                        # header is username. don't display display_name
                        width_username = draw.textsize(username, font=self.header1)[0]

                        draw.text(
                            ((image.size[0]-width_username) / 2, 290),
                            username,
                            (255, 255, 255),
                            font=self.header1
                        )
                    else:
                        # show both username and display name
                        width_display_name  = draw.textsize(display_name, font=self.header1)[0]
                        draw.text(
                            ((image.size[0]-width_display_name) / 2, 290),
                            display_name,
                            (240, 191, 60),
                            font=self.header1)

                        width_username = draw.textsize(username, font=self.header2)[0]
                        draw.text(
                            ((image.size[0]-width_username) / 2, 370),
                            username,
                            (255, 255, 255),
                            font=self.header2)

                else:
                    width_username = draw.textsize(username, font=self.header1)[0]

                    draw.text(
                        ((image.size[0]-width_username) / 2, 290),
                        username,
                        (255, 255, 255),
                        font=self.header1
                    )


            if description:
                if len(description) > 230:
                    description = f"{description[:230]}..."

                wrapper = TextWrapper(description, self.header4, image.width-70)
                wrapped_text = wrapper.wrapped_text()

                draw.text(
                    (40, 505),
                    wrapped_text,
                    (255, 255, 255),
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
