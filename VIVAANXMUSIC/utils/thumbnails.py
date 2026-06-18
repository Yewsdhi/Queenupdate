from PIL import Image, ImageDraw, ImageFont, ImageFilter
import requests
from io import BytesIO


async def generate_thumbnail(
    thumbnail_url: str,
    title: str,
    duration: str,
    output: str = "VivaanXMusic.png",
):
    # Download thumbnail
    response = requests.get(thumbnail_url)
    cover = Image.open(BytesIO(response.content)).convert("RGB")

    # Background
    bg = cover.resize((1280, 720))
    bg = bg.filter(ImageFilter.GaussianBlur(18))

    overlay = Image.new("RGBA", bg.size, (0, 0, 0, 120))
    bg = Image.alpha_composite(bg.convert("RGBA"), overlay)

    # Main Cover
    cover = cover.resize((520, 520))
    bg.paste(cover, (70, 100))

    draw = ImageDraw.Draw(bg)

    try:
        title_font = ImageFont.truetype("arial.ttf", 55)
        text_font = ImageFont.truetype("arial.ttf", 35)
        icon_font = ImageFont.truetype("arial.ttf", 75)
    except:
        title_font = ImageFont.load_default()
        text_font = ImageFont.load_default()
        icon_font = ImageFont.load_default()

    # Song Title
    title = title[:35]
    draw.text((650, 120), title, fill="white", font=title_font)

    # Bot Name
    draw.text(
        (650, 200),
        "🎵 VivaanXMusic",
        fill=(220, 220, 220),
        font=text_font,
    )

    # Progress Bar
    draw.line(
        (650, 290, 1180, 290),
        fill=(255, 255, 255),
        width=8,
    )

    draw.ellipse(
        (790, 275, 820, 305),
        fill="white",
    )

    draw.text(
        (650, 320),
        "0:03",
        fill="white",
        font=text_font,
    )

    draw.text(
        (1100, 320),
        f"-{duration}",
        fill="white",
        font=text_font,
    )

    # Controls
    draw.text((760, 410), "⏮", fill="white", font=icon_font)
    draw.text((870, 410), "⏸", fill="white", font=icon_font)
    draw.text((1010, 410), "⏭", fill="white", font=icon_font)

    # Volume Bar
    draw.line(
        (720, 560, 1100, 560),
        fill="white",
        width=8,
    )

    draw.text((670, 535), "🔈", fill="white", font=text_font)
    draw.text((1120, 535), "🔊", fill="white", font=text_font)

    # Footer
    draw.text(
        (820, 640),
        "Powered By VivaanXMusic",
        fill=(180, 180, 180),
        font=text_font,
    )

    bg.save(output)
    return output
