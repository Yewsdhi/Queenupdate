from PIL import Image, ImageDraw, ImageFont, ImageFilter
import requests
from io import BytesIO


async def get_thumb(thumb_url, title, duration):
    try:
        response = requests.get(thumb_url, timeout=10)
        image = Image.open(BytesIO(response.content)).convert("RGB")
    except Exception:
        image = Image.new("RGB", (1280, 720), (20, 20, 20))

    image = image.resize((1280, 720))

    # Blur Background
    bg = image.copy().filter(ImageFilter.GaussianBlur(15))

    # Dark Overlay
    overlay = Image.new("RGBA", bg.size, (0, 0, 0, 120))
    bg = Image.alpha_composite(bg.convert("RGBA"), overlay)

    draw = ImageDraw.Draw(bg)

    try:
        font_title = ImageFont.truetype("arial.ttf", 55)
        font_duration = ImageFont.truetype("arial.ttf", 40)
    except:
        font_title = ImageFont.load_default()
        font_duration = ImageFont.load_default()

    # Small Cover
    cover = image.resize((300, 300))
    bg.paste(cover, (100, 200))

    # Title
    draw.text(
        (450, 250),
        title[:40],
        fill="white",
        font=font_title,
    )

    # Duration
    draw.text(
        (450, 340),
        f"Duration: {duration}",
        fill="white",
        font=font_duration,
    )

    output = "thumbnail.png"
    bg.convert("RGB").save(output)

    return output
