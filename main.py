from telethon import TelegramClient, events
import subprocess
import io
import time
from PIL import Image
from myconf import *
import tools
import codecs

client = TelegramClient("telethon", api_id, api_hash)

# =================== spammer ====================#


@client.on(events.NewMessage(outgoing=True, pattern=r"&(\d+),?(\d*) (.*)"))
async def spammer(event):
    times, delay, text = event.pattern_match.groups()
    chatId = event.chat_id
    await event.delete()
    replyed = await event.get_reply_message()
    for i in range(int(times)):
        await client.send_message(chatId, text, reply_to=replyed)
        print("\r", i+1, "spam messages to", chatId, end="")
        if delay:
            time.sleep(int(delay))
    print()

# ================= base encoder =================#


@client.on(events.NewMessage(outgoing=True, pattern=r"&b(\d{2})\s(.*)"))
async def base_encoder(event):
    mode, text = event.pattern_match.groups()
    encoded = tools.b_encoder(text, mode)
    await event.edit(encoded)
    print("base" + mode, "encode of", text)

# ================= hex encoder ==================#


@client.on(events.NewMessage(outgoing=True, pattern=r'&hex\s'))
async def text2hex(event):
    message = event.raw_text
    text = message[4:].encode()
    encoded = codecs.encode(text, "hex").decode()
    await event.edit(encoded)
    print("hex encode of", encoded)

# ================ binary encoder ================#


@client.on(events.NewMessage(outgoing=True, pattern=r'&bin\s'))
async def text2bin(event):
    message = event.raw_text
    print(message)
    encoded = ' '.join(format(i, '08b') for i in bytearray(
        message.removeprefix(".bin "),
        encoding='utf-8'))
    await event.edit(encoded)
    print(encoded)

# ============== python code runner ==============#


@client.on(events.NewMessage(outgoing=True, pattern=r"&!"))
async def shell(event):
    message = event.raw_text
    code = message.removeprefix("&!")
    output = subprocess.getoutput(code)
    result = '🐡 <code>{}</code>\n\n{}'
    result = result.format(code, output)
    await event.edit(result)

# ============== python code runner ==============#


@client.on(events.NewMessage(outgoing=True, pattern=r"&py[\n\s]"))
async def python_runner(event):
    message = str(event.raw_text)
    code = str(message.removeprefix(message.split()[0]))[1:]
    output = subprocess.getoutput(
        'python -c "' + code.replace("\\", r"\\").replace("\"", r"\"") + '"')
    result = '🐍 <pre><code class="language_python">{}</code></pre>\n\n{}'
    result = result.format(code, output)
    await event.edit(result)

# ================ pic to sticker ================#


@client.on(events.NewMessage(outgoing=True, pattern=r"&(?:sticker|استیکر)"))
async def pic2sticker(event):
    chatId = event.chat_id
    replyed = await event.get_reply_message()

    img = Image.open(io.BytesIO(
        await client.download_media(
            event.message if event.message.media else replyed,
            file=bytes  # type: ignore
        )
    ))
    img.thumbnail((512, 512))
    with io.BytesIO() as img_bin:
        img.save(img_bin, "WEBP")
        img_bin.seek(0)
        img_bin.name = "sticker.webp"
        await client.send_file(chatId, img_bin, reply_to=replyed)
    print("sticker of photo")

# =============== text to sticker ================#


@client.on(events.NewMessage(outgoing=True, pattern=r"&s(#.{6})?\s"))
async def gen_sticker(event):
    await event.delete()
    message = event.raw_text
    replyed = await event.get_reply_message()
    chatId = event.chat_id
    prefix = message.split(" ")[0]
    text = " ".join(message.split(" ")[1:])
    color = prefix.removeprefix("&s") if "#" in prefix else "#893bff"
    img = tools.text2sticker(text, color)

    await client.send_file(chatId, img, reply_to=replyed)
    print(f"sticker of \"{text}\" sent to", chatId)


@client.on(events.NewMessage(outgoing=True, pattern=r"&khabi"))
async def gen_khabi_sticker(event):
    await event.delete()
    message = event.raw_text
    replyed = await event.get_reply_message()
    chatId = event.chat_id
    text = message.removeprefix("&khabi")
    color = "#893bff"  # default
    if text[0] == "#":
        color = text.split(" ")[0]
        text = " ".join(text.split(" ")[1:])
    img = tools.khabi_sticker(text, color)
    await client.send_file(chatId, img, reply_to=replyed)
    print(f"khabi sticker of \"{text}\" sent to", chatId)

# ================================================#


@client.on(events.NewMessage(outgoing=True, pattern=r"&cycle"))
async def cycler(event):
    def cycle(items):
        items = items.split()
        long = len(items)
        return [''.join(list(items*2)[i:i+long]) for i in range(long)]

    message = str(event.raw_text).removeprefix("&cycle ")

    i = 0
    while i < 100:
        for update in cycle(message):
            await event.edit(update)
            time.sleep(0.5)
            i += 1
            print(f"number {i} cycle", end="\r")
    print(f"number {i} cycle")

# ================================================#


@client.on(events.NewMessage(outgoing=True, pattern=r'boom'))
async def _(event):
    car = "                    🚗"
    for i in range(int(len(car) / 2)):
        time.sleep(0.5)
        await event.edit("🚧" + car[i * 2:])
    await event.edit("💥")
    print("online!")
    time.sleep(5)
    await event.delete()


client.start()
client.parse_mode = "html"
print("Running...")
client.run_until_disconnected()
