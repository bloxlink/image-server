from PIL import Image, ImageDraw

class TextWrapper(object):
    # Original algorithm: https://stackoverflow.com/questions/7698231/python-pil-draw-multiline-text-on-image
    # Algorithm modified by Julien Kmec

    """ Helper class to wrap text in lines, based on given text, font
        and max allowed line width.
    """

    def __init__(self, text, font, max_width, max_lines):
        self.text = text
        self.text_lines = [
            ' '.join([w.strip() for w in l.split(' ') if w])
            for l in text.split('\n')
            if l and l != "\n"
        ]
        self.font = font
        self.max_width = max_width
        self.max_lines = max_lines

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

        self.comma_width = self.draw.textsize(
            text=', ',
            font=self.font
        )[0]

    def get_text_width(self, text):
        return self.draw.textsize(
            text=text,
            font=self.font
        )[0]

    def wrapped_text(self):
        wrapped_lines = []
        current_line = []

        for line in self.text_lines:
            expected_line_width = 0

            for word in line.split(" "):
                word_width = self.get_text_width(word)

                if not expected_line_width:
                    expected_line_width = word_width
                else:
                    expected_line_width += word_width

                if expected_line_width <= self.max_width:
                    current_line.append(word)
                    expected_line_width += self.space_width
                else:
                    # start at next line and insert as much as possible
                    wrapped_lines.append("".join(current_line))
                    expected_line_width = 0
                    current_line = []

                    for char in word:
                        char_width = self.get_text_width(char)

                        # dash_width = self.dash_width if i != len(word) - 1 else 0

                        expected_line_width += char_width

                        if expected_line_width <= self.max_width:
                            current_line.append(char)
                        else:
                            current_line.append("-")
                            wrapped_lines.append("".join(current_line))
                            current_line = [char]
                            expected_line_width = 0

                current_line.append(" ")
                # expected_width += self.space_width

            wrapped_lines.append("".join(current_line))
            current_line = []

        if current_line:
            wrapped_lines.append("".join(current_line))

        if len(wrapped_lines) > self.max_lines:
            wrapped_lines[self.max_lines-1] = wrapped_lines[self.max_lines-1][:-3] + "..."

        wrapped_lines = wrapped_lines[:self.max_lines]

        return "\n".join(wrapped_lines), len(wrapped_lines)
