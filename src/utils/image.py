from PIL import Image, ImageDraw


def gradient_text(text, gradient_name, width, length, font=None):
    gradient_image = Image.open(f"./assets/gradients/{gradient_name}.jpg").resize((width, length))
    alpha = Image.new("L", (width, length))

    draw_alpha = ImageDraw.Draw(alpha)
    draw_alpha.text((0,0), text, fill="white", font=font)

    gradient_image.putalpha(alpha)

    alpha.close()

    return gradient_image
