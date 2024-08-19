from PIL import Image, ImageDraw, ImageFont
import io


def hex_to_rgb(color_hex: str) -> tuple:
    # "hex" should be a string, such as "#FFF" or "#FFFFFF"
    color_hex = color_hex.lstrip('#')
    rgb = tuple(int(color_hex[i:i+2], 16) for i in range(0, 6, 2))
    return rgb


def sticker_bin(img: Image) -> bytes:
    """
    takes PIL image type
    returns binary webp sticker
    """
    img.thumbnail((512, 512))
    img_bin = io.BytesIO()
    img.save(img_bin, "WEBP")
    img_bin.seek(0)
    img_bin.name = "sticker.webp"
    return img_bin


def text2sticker(text: str, color_hex: str) -> bytes:
    font = ImageFont.truetype("assets/Mikhak-Black.ttf", size=128)
    text_width, text_height = font.getbbox(text)[2:]
    img = Image.new("RGBA", (text_width+40, text_height+15), color=0)
    imgDraw = ImageDraw.Draw(img)
    color = hex_to_rgb(color_hex)
    imgDraw.text(
        (20, -15), text, fill=color, font=font,
        stroke_width=4, stroke_fill=(108, 48, 130)
    )
    return sticker_bin(img)


def khabi_sticker(text: str, color_hex: str) -> bytes:
    khabi_image = Image.open("assets/khabi.webp")
    khabi_image_x, khabi_image_y = khabi_image.size

    text_image = Image.open(text2sticker(text, color_hex))
    text_image_x, text_image_y = text_image.size

    new_image = Image.new("RGBA", (512, khabi_image_y+text_image_y))
    new_image.paste(khabi_image, (0, 0))
    text_start_x = int(int(khabi_image_x-text_image_x)/2)
    new_image.paste(text_image, (text_start_x, khabi_image_x-20))
    return sticker_bin(new_image)
