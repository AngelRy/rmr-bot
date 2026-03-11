# rmrbot/generator/image_generator.py

from PIL import Image, ImageDraw, ImageFont
import os
import random
from datetime import datetime
from rmrbot.config.settings import OUTPUT_DIR, LOGO_PATH, FONT_PATH

IMAGE_SIZE = (1080, 1080)

LOGO_SCALE = 0.15 
LOGO_PADDING = 30

MAX_FONT_SIZE = 64
MIN_FONT_SIZE = 28
LINE_SPACING = 10
MARGIN = 120
AUTHOR_FONT_SCALE = 0.6
AUTHOR_MARGIN_TOP = 20
GRADIENT_PALETTES = [
    # Red / Orange
    ((180, 50, 50), (220, 120, 60)),

    # Blue / Purple
    ((40, 70, 160), (120, 80, 200)),

    # Green / Teal
    ((40, 120, 90), (80, 180, 160)),

    # Dark gray / steel
    ((60, 60, 60), (120, 120, 120)),

    # Sunrise
    ((255, 120, 80), (255, 200, 120)),

    # Night run
    ((20, 30, 60), (70, 100, 140)),
]




def _wrap_text(text, font, max_width, draw):
    words = text.split()
    lines = []
    current = ""

    for word in words:
        test = f"{current} {word}".strip()
        bbox = draw.textbbox((0, 0), test, font=font)
        if bbox[2] <= max_width:
            current = test
        else:
            lines.append(current)
            current = word

    if current:
        lines.append(current)

    return lines


def generate_quote_image(quote: str, author: str | None = None) -> str:

    os.makedirs(OUTPUT_DIR, exist_ok=True)

    img = Image.new("RGB", IMAGE_SIZE)
    draw = ImageDraw.Draw(img)

    # Simple vertical gradient background
    # Gradient background (random palette)
    (top_color, bottom_color) = random.choice(GRADIENT_PALETTES)

    for y in range(IMAGE_SIZE[1]):
        ratio = y / IMAGE_SIZE[1]

        r = int(top_color[0] + ratio * (bottom_color[0] - top_color[0]))
        g = int(top_color[1] + ratio * (bottom_color[1] - top_color[1]))
        b = int(top_color[2] + ratio * (bottom_color[2] - top_color[2]))

        draw.line([(0, y), (IMAGE_SIZE[0], y)], fill=(r, g, b))


    max_text_width = IMAGE_SIZE[0] - 2 * MARGIN
    max_text_height = IMAGE_SIZE[1] - 2 * MARGIN

    font_size = MAX_FONT_SIZE

    while font_size >= MIN_FONT_SIZE:
        font = ImageFont.truetype(FONT_PATH, font_size)
        lines = _wrap_text(quote, font, max_text_width, draw)

        total_height = sum(
            draw.textbbox((0, 0), line, font=font)[3]
            for line in lines
        ) + LINE_SPACING * (len(lines) - 1)

        if total_height <= max_text_height:
            break

        font_size -= 2

    y = (IMAGE_SIZE[1] - total_height) // 2

    for line in lines:
        bbox = draw.textbbox((0, 0), line, font=font)
        x = (IMAGE_SIZE[0] - bbox[2]) // 2
        draw.text((x, y), line, font=font, fill="white")
        y += bbox[3] + LINE_SPACING


    if author:
        author_font_size = int(font_size * AUTHOR_FONT_SCALE)
        author_font = ImageFont.truetype(FONT_PATH, author_font_size)

        author_text = f"— {author}"
        bbox = draw.textbbox((0, 0), author_text, font=author_font)

        x = (IMAGE_SIZE[0] - bbox[2]) // 2
        y += AUTHOR_MARGIN_TOP

        draw.text((x, y), author_text, font=author_font, fill="white")

    # Add logo to bottom-right corner
    if os.path.exists(LOGO_PATH):
        try:
            logo = Image.open(LOGO_PATH).convert("RGBA")
        except Exception:
            logo = None

        target_w = int(IMAGE_SIZE[0] * LOGO_SCALE)
        ratio = target_w / logo.width
        target_h = int(logo.height * ratio)

        logo = logo.resize((target_w, target_h), Image.LANCZOS)

        x = IMAGE_SIZE[0] - target_w - LOGO_PADDING
        y_logo = IMAGE_SIZE[1] - target_h - LOGO_PADDING

        img.paste(logo, (x, y_logo), logo)


# ⬆⬆⬆ AUTHOR BLOCK ENDS HERE ⬆⬆⬆


    filename = f"quote_{datetime.now().strftime('%Y%m%d_%H%M%S_%f')}.png"
    path = os.path.join(OUTPUT_DIR, filename)
    img.save(path)

    return path
