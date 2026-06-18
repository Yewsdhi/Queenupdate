from PIL import Image, ImageDraw, ImageFont, ImageFilter
from io import BytesIO
import requests
import os

async def get_thumb(
thumb_url,
title,
duration,
output="thumb.png"
):
try:
r = requests.get(thumb_url, timeout=10)
cover = Image.open(BytesIO(r.content)).convert("RGB")

    # Background
    bg = cover.resize((1280, 720))
    bg = bg.filter(ImageFilter.GaussianBlur(25))

    overlay = Image.new("RGBA", bg.size, (0, 0, 0, 140))
    bg = Image.alpha_composite(bg.convert("RGBA"), overlay)

    # Cover
    cover = cover.resize((500, 500))
    bg.paste(cover, (80, 110))

    draw = ImageDraw.Draw(bg)

    try:
        title_font = ImageFont.truetype(
            "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf",
            55
        )
        text_font = ImageFont.truetype(
            "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf",
            35
        )
    except:
        title_font = ImageFont.load_default()
        text_font = ImageFont.load_default()

    # Title
    draw.text(
        (650, 120),
        str(title)[:30],
        fill="white",
        font=title_font
    )

    # Bot Name
    draw.text(
        (650, 200),
        "VIVAANXMUSIC",
        fill="white",
        font=text_font
    )

    # Duration
    draw.text(
        (650, 300),
        f"Duration : {duration}",
        fill="white",
        font=text_font
    )

    # Footer
    draw.text(
        (700, 650),
        "Powered By VIVAANXMUSIC",
        fill="white",
        font=text_font
    )

    bg = bg.convert("RGB")
    bg.save(output, quality=95)

    return output

except Exception as e:
    print("Thumbnail Error:", e)
    return None
