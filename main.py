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


@client.on(events.NewMessage(outgoing=True, pattern=r"&(\d+),?(\d*)\s(.*)"))
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


@client.on(events.NewMessage(outgoing=True, pattern=r'&hex\s(.*)'))
async def text2hex(event):
    text = event.pattern_match.group(1)
    encoded = codecs.encode(text, "hex").decode()
    await event.edit(encoded)
    print("hex encode of", encoded)

# ================ binary encoder ================#


@client.on(events.NewMessage(outgoing=True, pattern=r'&bin\s(.*)'))
async def text2bin(event):
    text = event.pattern_match.group(1)
    encoded = ' '.join(format(i, '08b')
                       for i in bytearray(text, encoding='utf-8'))
    await event.edit(encoded)
    print("sent binary of", text)

# ============== python code runner ==============#


@client.on(events.NewMessage(outgoing=True, pattern=r"&!\s?(.*)"))
async def shell(event):
    code = event.pattern_match.group(1)
    output = subprocess.getoutput(code)
    result = f"🐡 <code>{code}</code>\n\n{output}"
    await event.edit(result)

# ============== python code runner ==============#


@client.on(events.NewMessage(outgoing=True, pattern=r"&py\s(.*)"))
async def python_runner(event):
    code = event.pattern_match.group(1)
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


@client.on(events.NewMessage(outgoing=True, pattern=r"&s(#[\da-f]{6})?\s(.*)"))
async def gen_sticker(event):
    await event.delete()
    replyed = await event.get_reply_message()
    chatId = event.chat_id
    color, text = event.pattern_match.groups()
    if not color:
        color = "#893bff"
    img = tools.text2sticker(text, color)
    await client.send_file(chatId, img, reply_to=replyed)
    print(f'sticker of "{text}" sent to', chatId)


@client.on(events.NewMessage(outgoing=True, pattern=r"&khabi(#[\da-f]{6})?\s(.*)"))
async def gen_khabi_sticker(event):
    await event.delete()
    replyed = await event.get_reply_message()
    chatId = event.chat_id
    color, text = event.pattern_match.groups()
    if not color:
        color = "#893bff"  # default
    img = tools.khabi_sticker(text, color)
    await client.send_file(chatId, img, reply_to=replyed)
    print(f'khabi sticker of "{text}" sent to', chatId)

# ================================================#


@client.on(events.NewMessage(outgoing=True, pattern=r"&cycle\s(.*)"))
async def cycler(event):
    message = event.pattern_match.group(1)
    items = message.split()
    long = len(items)
    cycle = [''.join(list(items*2)[i:i+long]) for i in range(long)]

    i = 0
    while i < 100:
        for update in cycle:
            await event.edit(update)
            time.sleep(0.5)
            i += 1
            print(f"number {i} cycle", end="\r")
    print(f"number {i} cycle")

# ================================================#


@client.on(events.NewMessage(outgoing=True, pattern=r'pex'))
async def _(event):
    await event.edit("pex is emo!")
    print("online!")
    time.sleep(5)
    await event.delete()


client.start()
client.parse_mode = "html"
print("Running...")
client.run_until_disconnected()
