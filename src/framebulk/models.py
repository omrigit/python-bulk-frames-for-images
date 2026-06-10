from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Literal

TextPosition = Literal["auto", "top", "bottom", "left", "right"]
TextAlign = Literal["left", "center", "right"]
Orientation = Literal["portrait", "landscape"]


@dataclass(slots=True)
class FrameConfig:
    input_dir: Path
    output_dir: Path
    frame_color: str
    margin_top: int
    margin_right: int
    margin_bottom: int
    margin_left: int
    text: str
    text_position: TextPosition = "auto"
    text_align: TextAlign = "center"
    font_family: str | None = None
    font_path: Path | None = None
    font_size: int = 48
    min_font_size: int = 12
    text_color: str | None = None
    text_padding: int = 40
    jpeg_quality: int = 90
    preserve_metadata: bool = True
    suffix: str = "_framed"


@dataclass(slots=True)
class BatchResult:
    processed: int
    failed: int
    skipped: int

