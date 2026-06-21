import os
import aiohttp
import aiofiles
from PIL import Image, ImageDraw, ImageFilter, ImageEnhance, ImageFont
from youtubesearchpython.future import VideosSearch

CACHE_DIR = "cache"
os.makedirs(CACHE_DIR, exist_ok=True)

async def get_thumb(videoid):
    output = f"{CACHE_DIR}/{videoid}.png"

    if os.path.exists(output):
        return output

    try:
        search = VideosSearch(
            f"https://www.youtube.com/watch?v={videoid}",
            limit=1,
        )
        data = await search.next()
        result = data["result"][0]

        title = result["title"][:40]
        duration = result.get("duration", "Live")
        views = result.get("viewCount", {}).get("short", "Unknown")
        thumb_url = result["thumbnails"][0]["url"]

    except Exception:
        title = "Unknown Track"
        duration = "Live"
        views = "Unknown"
        thumb_url = f"https://i.ytimg.com/vi/{videoid}/hqdefault.jpg"

    thumb_file = f"{CACHE_DIR}/{videoid}_yt.jpg"

    async with aiohttp.ClientSession() as session:
        async with session.get(thumb_url) as resp:
            if resp.status == 200:
                async with aiofiles.open(thumb_file, "wb") as f:
                    await f.write(await resp.read())

    bg = Image.open(thumb_file).convert("RGBA")
    bg = bg.resize((1280, 720))
    bg = bg.filter(ImageFilter.GaussianBlur(20))
    bg = ImageEnhance.Brightness(bg).enhance(0.5)

    cover = Image.open(thumb_file).convert("RGBA")
    cover = cover.resize((450, 450))

    bg.paste(cover, (70, 135))

    draw = ImageDraw.Draw(bg)

    try:
        title_font = ImageFont.truetype(
            "VIVAANXMUSIC/assets/thumb/font2.ttf",
            42,
        )
        small_font = ImageFont.truetype(
            "VIVAANXMUSIC/assets/thumb/font.ttf",
            28,
        )
    except:
        title_font = ImageFont.load_default()
        small_font = ImageFont.load_default()

    draw.text(
        (580, 170),
        title,
        fill="white",
        font=title_font,
    )

    draw.text(
        (580, 240),
        f"👁 {views}",
        fill="white",
        font=small_font,
    )

    draw.text(
        (580, 290),
        f"⏱ {duration}",
        fill="white",
        font=small_font,
    )

    draw.line(
        (580, 360, 1100, 360),
        fill="white",
        width=8,
    )

    draw.line(
        (580, 360, 820, 360),
        fill="red",
        width=8,
    )

    draw.ellipse(
        (810, 350, 830, 370),
        fill="red",
    )

    draw.text(
        (650, 450),
        "⏮      ⏯      ⏭",
        fill="white",
        font=title_font,
    )

    draw.text(
        (580, 600),
        "🎵 Powered By VIVAAN MUSIC",
        fill="white",
        font=small_font,
    )

    bg.save(output)

    try:
        os.remove(thumb_file)
    except:
        pass

    return output
