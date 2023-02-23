from PIL import Image, ImageDraw, ImageFont
import io

def hex_to_rgb(hex):
    # "hex" should be a string, such as "#FFF" or "#FFFFFF"
    hex = hex.lstrip('#')
    hlen = len(hex)
    rgb = tuple(int(hex[i:i+hlen//3], 16) for i in range(0, hlen, hlen//3))
    return rgb

def getTextSize(text, font):
    img = Image.new("RGB", (512, 512))
    imgDraw = ImageDraw.Draw(img)
    return imgDraw.textbbox((0,0), text, font)[2:]

def textToSticker(text: str, color_hex: str):
    font = ImageFont.truetype("assets/Mikhak-Black.ttf", size=128)
    x, y = getTextSize(text, font)
    img = Image.new("RGBA", (x+40, y+15), color=0)
    imgDraw = ImageDraw.Draw(img)
    color = hex_to_rgb(color_hex)
    imgDraw.text((20, -15), text, fill=color, font=font, stroke_width=4, stroke_fill=(108, 48, 130))
    img.thumbnail((512, 512))
    img_bin = io.BytesIO()
    img.save(img_bin, "WEBP")
    img_bin.seek(0)
    img_bin.name = "sticker.webp"
    return img_bin

import base64, base58
def b_encoder(text, mod):
    text = text.encode()
    if mod == "85":
        encoded = base64.b85encode(text)
    elif mod == "64":
        encoded = base64.b64encode(text)
    elif mod == "58":
        encoded = base58.b58encode(text)
    elif mod == "32":
        encoded = base64.b32encode(text)
    else:
        encoded = b"Not supported!"
    return encoded.decode()
