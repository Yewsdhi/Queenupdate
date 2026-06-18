from PIL import Image, ImageDraw, ImageFont, ImageFilter
from io import BytesIO
import requests

async def get_thumb(
thumb_url,
title,
duration,
output="thumb.png"
):
try:
response = requests.get(thumb_url, timeout=10)
response.raise_for_status()

    cover = Image.open(
        BytesIO(response.content)
    ).convert("RGB")

    # Blur Background
    bg = cover.resize((1280, 720))
    bg = bg.filter(ImageFilter.GaussianBlur(25))

    overlay = Image.new(
        "RGBA",
        bg.size,
        (0, 0, 0, 140)
    )

    bg = Image.alpha_composite(
        bg.convert("RGBA"),
        overlay
    )

    # Album Cover
    album = cover.resize((500, 500))
    bg.paste(album, (80, 110))

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

    except Exception:
        title_font = ImageFont.load_default()
        text_font = ImageFont.load_default()

    # Song Title
    draw.text(
        (650, 120),
        str(title)[:30],
        fill="white",
        font=title_font
    )

    # Bot Name
    draw.text(
        (650, 210),
        "VIVAANXMUSIC",
        fill="white",
        font=text_font
    )

    # Progress Bar
    draw.line(
        (650, 300, 1180, 300),
        fill="white",
        width=8
    )

    draw.ellipse(
        (760, 285, 790, 315),
        fill="white"
    )

    # Duration
    draw.text(
        (650, 340),
        "0:03",
        fill="white",
        font=text_font
    )

    draw.text(
        (1080, 340),
        f"-{duration}",
        fill="white",
        font=text_font
    )

    # Controls
    draw.text(
        (760, 430),
        "<<",
        fill="white",
        font=title_font
    )

    draw.text(
        (900, 420),
        "||",
        fill="white",
        font=title_font
    )

    draw.text(
        (1030, 430),
        ">>",
        fill="white",
        font=title_font
    )

    # Footer
    draw.text(
        (720, 650),
        "Powered By VIVAANXMUSIC",
        fill=(220, 220, 220),
        font=text_font
    )

    bg = bg.convert("RGB")
    bg.save(output, quality=95)

    return output

except Exception as e:
    print(f"Thumbnail Error: {e}")
    return None
