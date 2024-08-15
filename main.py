from telethon import TelegramClient, events
import subprocess
import time
from myconf import api_id, api_hash
import tools

client = TelegramClient("telethon", api_id, api_hash)

# ================== spammer =================== #


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

# ============= python code runner ============= #


@client.on(events.NewMessage(outgoing=True, pattern=r"&!\s?(.*)"))
async def shell(event):
    code = event.pattern_match.group(1)
    output = subprocess.getoutput(code)
    result = f"🐡 <code>{code}</code>\n\n{output}"
    await event.edit(result)

# ============= python code runner ============= #


@client.on(events.NewMessage(outgoing=True, pattern=r"&py\s+(.*)"))
async def python_runner(event):
    code = event.pattern_match.group(1)
    process = subprocess.Popen(
        ['python'],
        stdin=subprocess.PIPE,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        universal_newlines=True,
    )
    output, error = process.communicate(input=code)
    result = '🐍 <pre><code class="language_python">{}</code></pre>\n\n{}'
    result = result.format(code, error or output)
    await event.edit(result)

# ================ conversions ================= #


@client.on(events.NewMessage(outgoing=True, pattern=r"&(p2s)"))
async def pic2sticker(event):
    await convertor(event, 'png', 'webp')
    print("photo to sticker")


@client.on(events.NewMessage(outgoing=True, pattern=r"&(s2g)"))
async def sticker2gif(event):
    await convertor(event, 'webm', 'gif')
    print("sticker to gif")


@client.on(events.NewMessage(outgoing=True, pattern=r"&(s2p)"))
async def sticker2pic(event):
    await convertor(event, 'webp', 'png')
    print("sticker to pic")


@client.on(events.NewMessage(outgoing=True, pattern=r"&(g2s)"))
async def gif2sticker(event):
    await convertor(
        event, 'mp4', 'webm',
        ['-r', '24', '-ss', '00:00', '-to', '00:03',
         '-c:v', 'libvpx-vp9', '-vf', 'scale=512:-2',
         '-an', '-loop', '0']
    )
    print("gif to sticker")


async def convertor(
        event,
        input_ext: str,
        output_ext: str,
        convert_options=[]
):
    chatId = event.chat_id
    replyed = await event.get_reply_message()

    input_file = "cache/input." + input_ext
    output_file = "cache/output." + output_ext
    await client.download_media(
        event.message if event.message.media else replyed,
        file=input_file
    )
    ffmpeg_cmd = ['ffmpeg', '-i', input_file, '-y',
                  '-v', 'error'] + convert_options + [output_file]
    subprocess.run(ffmpeg_cmd)

    await event.edit("uploading...")
    await client.send_file(chatId, output_file, reply_to=replyed)

# ============== text to sticker =============== #


@client.on(events.NewMessage(
    outgoing=True,
    pattern=r"&(s|س)(#[\da-f]{6})?\s(.*)")
)
async def gen_sticker(event):
    await event.delete()
    replyed = await event.get_reply_message()
    chatId = event.chat_id
    _, color, text = event.pattern_match.groups()
    if not color:
        color = "#893bff"
    img = tools.text2sticker(text, color)
    await client.send_file(chatId, img, reply_to=replyed)
    print(f'sticker of "{text}" sent to', chatId)


@client.on(events.NewMessage(
    outgoing=True,
    pattern=r"&khabi(#[\da-f]{6})?\s(.*)")
)
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

# ============================================== #


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

# ============================================== #


@client.on(events.NewMessage(outgoing=True, pattern=r'pxe'))
async def _(event):
    await event.edit("pxe is emo!")
    print("online!")
    time.sleep(5)
    await event.delete()


client.start()
client.parse_mode = "html"
print("Running...")
client.run_until_disconnected()
