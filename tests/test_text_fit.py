from pathlib import Path

import pytest
from PIL import Image, ImageDraw

from framebulk.image_ops import _fit_font_size, default_text_color, parse_color, text_coordinates, validate_config
from framebulk.models import FrameConfig


def test_default_text_color_contrast() -> None:
    assert default_text_color("white") == "black"
    assert default_text_color("black") == "white"


def test_parse_color_hex() -> None:
    assert parse_color("#ffffff") == (255, 255, 255)


def test_fit_font_size_shrinks_for_long_text() -> None:
    config = FrameConfig(
        input_dir=Path("."),
        output_dir=Path("."),
        frame_color="white",
        margin_top=50,
        margin_right=50,
        margin_bottom=100,
        margin_left=50,
        text="this is a very very very long text that should shrink",
        font_size=48,
        min_font_size=12,
    )
    image = Image.new("RGB", (400, 200), "white")
    draw = ImageDraw.Draw(image)
    size = _fit_font_size(draw, config.text, max_width=120, config=config)
    assert 12 <= size <= 48
    assert size < 48


def test_text_coordinates_top_bottom_alignment() -> None:
    x_left, _ = text_coordinates(
        x=100,
        y=0,
        box_w=200,
        box_h=100,
        text_w=50,
        text_h=20,
        align="left",
        position="top",
    )
    x_center, _ = text_coordinates(
        x=100,
        y=0,
        box_w=200,
        box_h=100,
        text_w=50,
        text_h=20,
        align="center",
        position="top",
    )
    x_right, _ = text_coordinates(
        x=100,
        y=0,
        box_w=200,
        box_h=100,
        text_w=50,
        text_h=20,
        align="right",
        position="top",
    )
    assert x_left == 100
    assert x_center == 175
    assert x_right == 250


def test_validate_config_invalid_color_has_suggestion() -> None:
    config = FrameConfig(
        input_dir=Path("."),
        output_dir=Path("."),
        frame_color="whiet",
        margin_top=50,
        margin_right=50,
        margin_bottom=50,
        margin_left=50,
        text="hello",
    )
    with pytest.raises(ValueError, match="Invalid frame color 'whiet'"):
        validate_config(config)


def test_validate_config_invalid_font_has_actionable_error() -> None:
    config = FrameConfig(
        input_dir=Path("."),
        output_dir=Path("."),
        frame_color="white",
        margin_top=50,
        margin_right=50,
        margin_bottom=50,
        margin_left=50,
        text="hello",
        font_family="not-a-real-font-name-12345",
    )
    with pytest.raises(ValueError, match="list-fonts --contains"):
        validate_config(config)

