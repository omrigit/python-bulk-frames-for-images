from __future__ import annotations

from dataclasses import replace
from difflib import get_close_matches
from typing import Literal

from PIL import Image, ImageColor, ImageDraw, ImageOps

from framebulk.fonts import FONT_EXTENSIONS, find_system_font, list_system_fonts, load_font
from framebulk.models import FrameConfig, Orientation, TextAlign, TextPosition


def normalize_image(image: Image.Image) -> Image.Image:
    return ImageOps.exif_transpose(image)


def classify_orientation(width: int, height: int) -> Orientation:
    return "portrait" if height > width else "landscape"


def resolve_text_position(text_position: TextPosition, orientation: Orientation) -> TextPosition:
    _ = orientation
    return text_position


def parse_color(color: str) -> tuple[int, int, int]:
    rgb = ImageColor.getrgb(color)
    if len(rgb) == 4:
        return rgb[:3]
    return rgb


def default_text_color(frame_color: str) -> str:
    return "black" if frame_color.lower() == "white" else "white"


def _validate_color(value: str, label: str) -> None:
    try:
        parse_color(value)
    except ValueError as exc:
        normalized = value.strip().lower()
        suggestions = get_close_matches(normalized, sorted(ImageColor.colormap.keys()), n=4, cutoff=0.6)
        message = f"Invalid {label} '{value}'. Use a named color (e.g. white, black, gold) or hex like #RRGGBB."
        if suggestions:
            message += f" Did you mean: {', '.join(suggestions)}?"
        raise ValueError(message) from exc


def _validate_and_resolve_font(config: FrameConfig) -> FrameConfig:
    if config.font_path:
        if not config.font_path.exists():
            raise ValueError(f"Font path does not exist: {config.font_path}")
        if config.font_path.suffix.lower() not in FONT_EXTENSIONS:
            exts = ", ".join(FONT_EXTENSIONS)
            raise ValueError(f"Invalid font file extension for '{config.font_path.name}'. Expected one of: {exts}")
        try:
            load_font(config.font_size, font_path=config.font_path)
        except OSError as exc:
            raise ValueError(f"Could not load font file: {config.font_path}. ({exc})") from exc
        return config

    if config.font_family:
        resolved = find_system_font(config.font_family)
        if resolved is None:
            available_names = [name for name, _ in list_system_fonts(include_arabic=False)]
            suggestions = get_close_matches(config.font_family, available_names, n=5, cutoff=0.5)
            message = (
                f"Font '{config.font_family}' was not found. "
                "Run 'framebulk list-fonts --contains <part-of-name>' to discover valid fonts."
            )
            if suggestions:
                message += f" Suggestions: {', '.join(suggestions)}."
            raise ValueError(message)
        return replace(config, font_path=resolved)
    return config


def _fit_font_size(
    draw: ImageDraw.ImageDraw,
    text: str,
    max_width: int,
    config: FrameConfig,
) -> int:
    for font_size in range(config.font_size, config.min_font_size - 1, -1):
        font = load_font(font_size, font_path=config.font_path, font_family=config.font_family)
        bbox = draw.textbbox((0, 0), text, font=font)
        if (bbox[2] - bbox[0]) <= max_width:
            return font_size
    return config.min_font_size


def apply_frame_and_text(image: Image.Image, config: FrameConfig) -> Image.Image:
    normalized = normalize_image(image).convert("RGB")
    width, height = normalized.size
    orientation = classify_orientation(width, height)
    position = resolve_text_position(config.text_position, orientation)

    out_w = width + config.margin_left + config.margin_right
    out_h = height + config.margin_top + config.margin_bottom
    framed = Image.new("RGB", (out_w, out_h), color=parse_color(config.frame_color))
    framed.paste(normalized, (config.margin_left, config.margin_top))

    if not config.text:
        return framed

    draw = ImageDraw.Draw(framed)
    text_color = parse_color(config.text_color or default_text_color(config.frame_color))

    region = text_region(
        out_w=out_w,
        out_h=out_h,
        image_w=width,
        image_h=height,
        margin_top=config.margin_top,
        margin_right=config.margin_right,
        margin_bottom=config.margin_bottom,
        margin_left=config.margin_left,
        requested_position=position,
        orientation=orientation,
    )
    x, y, box_w, box_h, resolved_position = region
    if box_w <= 0 or box_h <= 0:
        return framed

    max_line_width = max((box_w - 10) if resolved_position in ("top", "bottom") else (out_w - 10), 1)
    font_size = _fit_font_size(draw, config.text, max_width=max_line_width, config=config)
    font = load_font(font_size, font_path=config.font_path, font_family=config.font_family)
    bbox = draw.textbbox((0, 0), config.text, font=font)
    text_w = bbox[2] - bbox[0]
    text_h = bbox[3] - bbox[1]

    text_x, text_y = text_coordinates(
        x=x,
        y=y,
        box_w=box_w,
        box_h=box_h,
        text_w=text_w,
        text_h=text_h,
        align=config.text_align,
        position=resolved_position,
    )
    draw.text((text_x, text_y), config.text, fill=text_color, font=font)
    return framed


def text_region(
    *,
    out_w: int,
    out_h: int,
    image_w: int,
    image_h: int,
    margin_top: int,
    margin_right: int,
    margin_bottom: int,
    margin_left: int,
    requested_position: Literal["top", "bottom", "left", "right"],
    orientation: Orientation,
) -> tuple[int, int, int, int, Literal["top", "bottom", "left", "right"]]:
    regions: dict[Literal["top", "bottom", "left", "right"], tuple[int, int, int, int]] = {
        "top": (margin_left, 0, image_w, margin_top),
        "bottom": (margin_left, margin_top + image_h, image_w, margin_bottom),
        "left": (0, margin_top, margin_left, image_h),
        "right": (margin_left + image_w, margin_top, margin_right, image_h),
    }
    if requested_position == "auto":
        scored: list[tuple[int, int, Literal["top", "bottom", "left", "right"]]] = []
        priority = {"bottom": 0, "top": 1, "left": 2, "right": 3}
        for pos, (_, _, w, h) in regions.items():
            if w <= 0 or h <= 0:
                continue
            scored.append((w * h, -priority[pos], pos))
        if scored:
            scored.sort(reverse=True)
            best = scored[0][2]
            x, y, w, h = regions[best]
            return (x, y, w, h, best)
        return (0, 0, 0, 0, "bottom")

    if requested_position in regions:
        preferred = regions[requested_position]
        if preferred[2] > 0 and preferred[3] > 0:
            return (*preferred, requested_position)

    for position in ("bottom", "top", "left", "right"):
        region = regions[position]
        if region[2] > 0 and region[3] > 0:
            return (*region, position)
    return (0, 0, 0, 0, "bottom")


def text_coordinates(
    *,
    x: int,
    y: int,
    box_w: int,
    box_h: int,
    text_w: int,
    text_h: int,
    align: TextAlign,
    position: Literal["top", "bottom", "left", "right"],
) -> tuple[int, int]:
    if position in ("top", "bottom"):
        if align == "left":
            text_x = x
        elif align == "right":
            text_x = x + max(box_w - text_w, 0)
        else:
            text_x = x + max((box_w - text_w) // 2, 0)
        text_y = y + max((box_h - text_h) // 2, 0)
        return text_x, text_y

    # For side regions, use align along vertical axis:
    # left -> top, center -> middle, right -> bottom.
    text_x = x + max((box_w - text_w) // 2, 0)
    if align == "left":
        text_y = y
    elif align == "right":
        text_y = y + max(box_h - text_h, 0)
    else:
        text_y = y + max((box_h - text_h) // 2, 0)
    return text_x, text_y


def validate_config(config: FrameConfig) -> FrameConfig:
    config = replace(config)
    margins = [config.margin_top, config.margin_right, config.margin_bottom, config.margin_left]
    if any(m < 0 for m in margins):
        raise ValueError("Margins must be >= 0.")
    if config.font_size < 1:
        raise ValueError("Font size must be >= 1.")
    if config.min_font_size < 1:
        raise ValueError("Min font size must be >= 1.")
    if config.min_font_size > config.font_size:
        raise ValueError("Min font size cannot exceed font size.")
    if not 1 <= config.jpeg_quality <= 100:
        raise ValueError("JPEG quality must be between 1 and 100.")
    if config.text_align not in ("left", "center", "right"):
        raise ValueError("Text align must be one of: left, center, right.")
    _validate_color(config.frame_color, "frame color")
    _validate_color(config.text_color or default_text_color(config.frame_color), "text color")
    return _validate_and_resolve_font(config)

