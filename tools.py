import base58
import base64
from PIL import Image, ImageDraw, ImageFont
import io


def hex_to_rgb(color_hex: str):
    # "hex" should be a string, such as "#FFF" or "#FFFFFF"
    color_hex = color_hex.lstrip('#')
    rgb = tuple(int(color_hex[i:i+2], 16) for i in range(0, 6, 2))
    return rgb

# format PIL image to binary webp sticker


def sticker_bin(img):
    img.thumbnail((512, 512))
    img_bin = io.BytesIO()
    img.save(img_bin, "WEBP")
    img_bin.seek(0)
    img_bin.name = "sticker.webp"
    return img_bin


def get_text_size(text, font):
    img = Image.new("RGB", (512, 512))
    imgDraw = ImageDraw.Draw(img)
    return imgDraw.textbbox((0, 0), text, font)[2:]


def text2sticker(text: str, color_hex: str):
    font = ImageFont.truetype("assets/Mikhak-Black.ttf", size=128)
    x, y = get_text_size(text, font)
    img = Image.new("RGBA", (x+40, y+15), color=0)
    imgDraw = ImageDraw.Draw(img)
    color = hex_to_rgb(color_hex)
    imgDraw.text((20, -15), text, fill=color, font=font,
                 stroke_width=4, stroke_fill=(108, 48, 130))
    return sticker_bin(img)


def khabi_sticker(text: str, color_hex: str):
    khabi_image = Image.open("assets/khabi.webp")
    khabi_image_x, khabi_image_y = khabi_image.size

    text_image = Image.open(text2sticker(text, color_hex))
    text_image_x, text_image_y = text_image.size

    new_image = Image.new("RGBA", (512, khabi_image_y+text_image_y))
    new_image.paste(khabi_image, (0, 0))
    text_start_x = int(int(khabi_image_x-text_image_x)/2)
    new_image.paste(text_image, (text_start_x, khabi_image_x-20))
    return sticker_bin(new_image)


def b_encoder(text, mode):
    text = text.encode()
    if mode == "85":
        encoded = base64.b85encode(text)
    elif mode == "64":
        encoded = base64.b64encode(text)
    elif mode == "58":
        encoded = base58.b58encode(text)
    elif mode == "32":
        encoded = base64.b32encode(text)
    else:
        encoded = b"Not supported!"
    return encoded.decode()
