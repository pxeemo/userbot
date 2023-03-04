from PIL import Image, ImageDraw, ImageFont
import io

def hex_to_rgb(hex):
    # "hex" should be a string, such as "#FFF" or "#FFFFFF"
    hex = hex.lstrip('#')
    hlen = len(hex)
    rgb = tuple(int(hex[i:i+hlen//3], 16) for i in range(0, hlen, hlen//3))
    return rgb

def sticker_bin(img):
    # format PIL image to binary webp sticker
    img.thumbnail((512, 512))
    img_bin = io.BytesIO()
    img.save(img_bin, "WEBP")
    img_bin.seek(0)
    img_bin.name = "sticker.webp"
    return img_bin

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
    return sticker_bin(img)

def khabi_sticker(text: str, color_hex: str):
    text_img = Image.open(textToSticker(text, color_hex))
    text_img_x, text_img_y = text_img.size
    khabi = Image.open("assets/khabi.webp")
    new = Image.new("RGBA", (text_img_x + 300, 512))
    new.paste(khabi, (0, 0))
    new.paste(text_img, (300, 450 - text_img_y))
    return sticker_bin(new)


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
