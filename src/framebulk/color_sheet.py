from __future__ import annotations

from math import ceil
from pathlib import Path

from PIL import Image, ImageColor, ImageDraw, ImageFont


def generate_color_cheatsheet(output_path: Path) -> Path:
    color_names = sorted(ImageColor.colormap.keys())
    columns = 4
    swatch_width = 340
    swatch_height = 56
    title_height = 80
    rows = ceil(len(color_names) / columns)
    width = columns * swatch_width
    height = title_height + rows * swatch_height + 20

    image = Image.new("RGB", (width, height), "white")
    draw = ImageDraw.Draw(image)
    font = ImageFont.load_default()

    draw.text((20, 16), "framebulk color cheatsheet (all PIL named colors)", fill="black", font=font)
    draw.text((20, 36), f"total colors: {len(color_names)}", fill="gray", font=font)

    for idx, name in enumerate(color_names):
        col = idx % columns
        row = idx // columns
        x = col * swatch_width
        y = title_height + row * swatch_height
        rgb = ImageColor.getrgb(name)
        text_color = "black" if sum(rgb[:3]) > 380 else "white"
        draw.rectangle((x + 8, y + 8, x + swatch_width - 8, y + swatch_height - 8), fill=rgb, outline="black")
        draw.text((x + 14, y + 22), name, fill=text_color, font=font)

    output_path.parent.mkdir(parents=True, exist_ok=True)
    image.save(output_path, format="JPEG", quality=95)
    return output_path

