from __future__ import annotations

from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

from framebulk.fonts import detect_font_script, list_system_fonts

OUTPUT_PATH = Path("out/font-cheatsheet.png")
TITLE = "framebulk font cheat sheet"
LATIN_SAMPLE = "The quick brown fox 0123456789"
HEBREW_SAMPLE = "זה טקסט בדיקה בעברית 0123456789"
ARABIC_SAMPLE = "هذا نص تجريبي بالعربية 0123456789"


def safe_font(candidates: list[str | Path], size: int) -> ImageFont.FreeTypeFont | ImageFont.ImageFont:
    for candidate in candidates:
        try:
            return ImageFont.truetype(str(candidate), size)
        except OSError:
            continue
    return ImageFont.load_default()


def sample_for_font(path: Path) -> tuple[str, str]:
    script = detect_font_script(path)
    if script == "hebrew":
        return ("hebrew", HEBREW_SAMPLE)
    if script == "arabic":
        return ("arabic", ARABIC_SAMPLE)
    return (script, LATIN_SAMPLE)


def render_cheatsheet() -> Path:
    fonts = list_system_fonts(include_arabic=False)
    if not fonts:
        raise RuntimeError("No fonts found.")

    preview_fonts = fonts[:80]
    row_height = 78
    width = 1600
    height = 90 + (len(preview_fonts) * row_height) + 20

    image = Image.new("RGB", (width, height), "white")
    draw = ImageDraw.Draw(image)
    preferred_title_candidates: list[str | Path] = [
        "DejaVuSans.ttf",
        "Arial.ttf",
        fonts[0][1],
    ]
    title_font = safe_font(preferred_title_candidates, 32)
    meta_font = safe_font(preferred_title_candidates, 18)
    draw.text((24, 20), TITLE, fill="black", font=title_font)
    draw.text((24, 58), f"showing {len(preview_fonts)} fonts", fill="gray", font=meta_font)

    y = 90
    for index, (name, path) in enumerate(preview_fonts):
        row_bg = (248, 248, 248) if index % 2 == 0 else (255, 255, 255)
        draw.rectangle((0, y - 4, width, y + row_height - 8), fill=row_bg)

        script_tag, sample_text = sample_for_font(path)
        label = f"{name} [{script_tag}] ({path.name})"
        draw.text((24, y), label, fill=(30, 30, 30), font=meta_font)

        try:
            sample_font = ImageFont.truetype(str(path), 34)
        except OSError:
            sample_font = ImageFont.load_default()

        draw.text((560, y - 4), sample_text, fill="black", font=sample_font)
        y += row_height

    OUTPUT_PATH.parent.mkdir(parents=True, exist_ok=True)
    image.save(OUTPUT_PATH)
    return OUTPUT_PATH


if __name__ == "__main__":
    output = render_cheatsheet()
    print(f"Created {output}")

