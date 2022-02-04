from PIL import Image, ImageDraw

class TextWrapper(object):
    # https://stackoverflow.com/questions/7698231/python-pil-draw-multiline-text-on-image
    # Algorithm modified by Julien Kmec

    """ Helper class to wrap text in lines, based on given text, font
        and max allowed line width.
    """

    def __init__(self, text, font, max_width):
        self.text = text
        self.text_lines = [
            ' '.join([w.strip() for w in l.split(' ') if w])
            for l in text.split('\n')
            if l and l != "\n"
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

        self.dash_width = self.draw.textsize(
            text='-',
            font=self.font
        )[0]

    def get_text_width(self, text):
        return self.draw.textsize(
            text=text,
            font=self.font
        )[0]

    def wrapped_text(self):
        wrapped_lines = []
        expected_width = 0
        current_line = []

        for line in self.text_lines:
            for word in line.split(' '):

                for i, char in enumerate(word):
                    char_width = self.get_text_width(char)

                    if not expected_width:
                        expected_width = char_width

                    dash_width = self.dash_width if i != len(word) - 1 else 0

                    if expected_width + dash_width <= self.max_width:
                        current_line.append(char)
                        expected_width += char_width
                    else:
                        current_line.append("-")
                        wrapped_lines.append("".join(current_line))
                        current_line = [char]
                        expected_width = 0

                current_line.append(" ")
                expected_width += self.space_width

            wrapped_lines.append("".join(current_line))
            current_line = []
            expected_width = 0

        if current_line:
            wrapped_lines.append("".join(current_line))

        if len(wrapped_lines) > 10:
            wrapped_lines[9] = wrapped_lines[9][:-3] + "..."

        wrapped_lines = wrapped_lines[:8]

        return "\n".join(wrapped_lines)
