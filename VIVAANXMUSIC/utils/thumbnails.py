from PIL import Image, ImageDraw, ImageFont, ImageFilter
from io import BytesIO
import requests


async def get_thumb(
    thumb_url,
    title,
    duration,
    output="thumb.png"
):
    response = requests.get(thumb_url, timeout=10)
    cover = Image.open(BytesIO(response.content)).convert("RGB")

    # Blur Background
    bg = cover.resize((1280, 720))
    bg = bg.filter(ImageFilter.GaussianBlur(20))

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

    # Cover
    cover = cover.resize((500, 500))
    bg.paste(cover, (80, 110))

    # Black Overlay
    overlay = Image.new("RGBA", bg.size, (0, 0, 0, 120))
    bg = Image.alpha_composite(bg.convert("RGBA"), overlay)

    draw = ImageDraw.Draw(bg)

    # Song Title
    draw.text(
        (650, 120),
        title[:30],
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

    # Progress Bar
    draw.line(
        (650, 280, 1180, 280),
        fill="white",
        width=8
    )

    draw.ellipse(
        (760, 265, 790, 295),
        fill="white"
    )

    draw.text(
        (650, 310),
        "0:03",
        fill="white",
        font=text_font
    )

    draw.text(
        (1100, 310),
        f"-{duration}",
        fill="white",
        font=text_font
    )

    # Controls
    draw.text(
        (780, 400),
        "<<",
        fill="white",
        font=title_font
    )

    draw.text(
        (900, 390),
        "||",
        fill="white",
        font=title_font
    )

    draw.text(
        (1020, 400),
        ">>",
        fill="white",
        font=title_font
    )

    bg = bg.convert("RGB")
    bg.save(output)

    return output
