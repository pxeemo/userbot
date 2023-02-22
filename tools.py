from PIL import Image, ImageDraw, ImageFont
import io

def getTextSize(text, font):
    img = Image.new("RGB", (512, 512))
    imgDraw = ImageDraw.Draw(img)
    return imgDraw.textbbox((0,0), text, font)[2:]

def textToSticker(text):
    font = ImageFont.truetype("assets/Lalezar-Regular.ttf", size=128)
    x, y = getTextSize(text, font)
    img = Image.new("RGBA", (x+40, y+5), color=0)
    imgDraw = ImageDraw.Draw(img)
    imgDraw.text((20, -15), text, fill="purple", font=font, stroke_width=6, stroke_fill="orange")
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
