from __future__ import annotations

import hashlib
from pathlib import Path
from typing import Literal

from PIL import ImageFont

FONT_EXTENSIONS = (".ttf", ".otf", ".ttc")
PROJECT_BUNDLED_FONT_DIR = Path(__file__).resolve().parents[2] / "assets" / "fonts"
FONT_DIRS = (
    PROJECT_BUNDLED_FONT_DIR,
    Path("/System/Library/Fonts"),
    Path("/Library/Fonts"),
    Path.home() / "Library/Fonts",
)


def _glyph_digest(font: ImageFont.FreeTypeFont | ImageFont.ImageFont, char: str) -> str:
    mask = font.getmask(char)
    return hashlib.md5(bytes(mask)).hexdigest()


def _supports_probe(font: ImageFont.FreeTypeFont | ImageFont.ImageFont, probe: str) -> bool:
    chars = [ch for ch in probe if not ch.isspace()]
    if len(chars) < 2:
        return False
    digests = [_glyph_digest(font, ch) for ch in chars]
    return len(set(digests)) > 1


def detect_font_script(path: Path) -> Literal["latin", "hebrew", "arabic", "mixed", "unknown"]:
    try:
        font = ImageFont.truetype(str(path), size=24)
    except OSError:
        return "unknown"

    has_latin = _supports_probe(font, "Abg")
    has_hebrew = _supports_probe(font, "אבג")
    has_arabic = _supports_probe(font, "مرح")

    if has_arabic and not has_latin and not has_hebrew:
        return "arabic"
    if has_latin and has_hebrew and has_arabic:
        return "mixed"
    if has_latin:
        return "latin"
    if has_hebrew:
        return "hebrew"
    if has_arabic:
        return "arabic"
    return "unknown"


def list_system_fonts(include_arabic: bool = False) -> list[tuple[str, Path]]:
    seen: set[str] = set()
    fonts: list[tuple[str, Path]] = []
    for base in FONT_DIRS:
        if not base.exists():
            continue
        for path in base.rglob("*"):
            if path.suffix.lower() not in FONT_EXTENSIONS:
                continue
            name = path.stem
            key = name.lower()
            if key in seen:
                continue
            if not include_arabic and detect_font_script(path) == "arabic":
                continue
            seen.add(key)
            fonts.append((name, path))
    fonts.sort(key=lambda item: item[0].lower())
    return fonts


def find_system_font(font_family: str) -> Path | None:
    query = font_family.strip().lower()
    if not query:
        return None

    for name, path in list_system_fonts(include_arabic=False):
        stem = name.lower()
        file_name = path.name.lower()
        if query == stem or query in stem or query in file_name:
            return path
    return None


def load_font(
    font_size: int,
    font_path: Path | None = None,
    font_family: str | None = None,
) -> ImageFont.FreeTypeFont | ImageFont.ImageFont:
    if font_path:
        return ImageFont.truetype(str(font_path), size=font_size)

    if font_family:
        family_path = find_system_font(font_family)
        if family_path is not None:
            return ImageFont.truetype(str(family_path), size=font_size)
        try:
            return ImageFont.truetype(font_family, size=font_size)
        except OSError:
            raise ValueError(
                f"Font '{font_family}' was not found. "
                "Run 'framebulk list-fonts' to see available fonts, "
                "or pass --font-path to a .ttf/.otf/.ttc file."
            ) from None

    # Prefer Unicode-capable defaults before falling back to bitmap default.
    for fallback_name in ("DejaVuSans.ttf", "Arial Unicode.ttf", "Arial Unicode MS.ttf"):
        try:
            return ImageFont.truetype(fallback_name, size=font_size)
        except OSError:
            continue

    return ImageFont.load_default()

