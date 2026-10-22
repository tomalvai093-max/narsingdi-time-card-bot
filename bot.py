import os
import io
import math
import asyncio
from datetime import datetime
from zoneinfo import ZoneInfo

import requests
from PIL import Image, ImageDraw, ImageFont
from telegram import Bot

TOKEN = os.environ["BOT_TOKEN"]
CHAT_ID = os.environ["CHAT_ID"]
TZ = ZoneInfo("Asia/Dhaka")

def make_clock():
    now = datetime.now(TZ)
    w, h = 1000, 500
    im = Image.new("RGB", (w, h), "#080b12")
    d = ImageDraw.Draw(im)

    d.rounded_rectangle((20, 20, 980, 480), 38,
                        fill="#111722", outline="#273448", width=3)

    def font(size, bold=False):
        paths = [
            "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
            if bold else
            "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"
        ]
        for path in paths:
            if os.path.exists(path):
                return ImageFont.truetype(path, size)
        return ImageFont.load_default()

    d.text((65, 65), "BANGLADESH • LIVE TIME",
           font=font(28, True), fill="#8da9c9")

    time_text = now.strftime("%I:%M %p").lstrip("0")
    d.text((60, 145), time_text,
           font=font(100, True), fill="#ffffff")

    d.text((65, 285), "Narsingdi, Bangladesh",
           font=font(34), fill="#8fdcff")
    d.text((65, 350), now.strftime("%A, %d %B %Y"),
           font=font(25), fill="#b6c1d2")

    cx, cy, r = 790, 255, 125
    d.ellipse((cx-r, cy-r, cx+r, cy+r),
              fill="#080d16", outline="#4b6688", width=5)

    for i in range(12):
        a = math.radians(i * 30 - 90)
        x1, y1 = cx + math.cos(a)*103, cy + math.sin(a)*103
        x2, y2 = cx + math.cos(a)*113, cy + math.sin(a)*113
        d.line((x1, y1, x2, y2), fill="#dce8fa", width=4)

    hour = (now.hour % 12) + now.minute / 60
    minute = now.minute + now.second / 60

    for value, length, width in [(hour, 62, 8), (minute, 88, 5)]:
        a = math.radians(value * 30 - 90) if length == 62 else math.radians(value * 6 - 90)
        d.line((cx, cy, cx + math.cos(a)*length,
                cy + math.sin(a)*length), fill="#ffffff", width=width)

    d.ellipse((cx-7, cy-7, cx+7, cy+7), fill="#8fdcff")

    d.text((65, 425), "TIMEZONE  ASIA/DHAKA  •  UTC+06:00",
           font=font(20), fill="#72849e")

    out = io.BytesIO()
    im.save(out, format="PNG")
    out.seek(0)
    return out, now

async def main():
    image, now = make_clock()
    async with Bot(TOKEN) as bot:
        await bot.send_photo(
            chat_id=CHAT_ID,
            photo=image,
            caption="🕒 Narsingdi Time • " + now.strftime("%I:%M %p")
        )

if __name__ == "__main__":
    asyncio.run(main())
