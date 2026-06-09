from pathlib import Path

from framebulk.models import FrameConfig
from framebulk.processor import build_save_kwargs, is_supported_image, output_path_for


def test_supported_extension_detection(tmp_path: Path) -> None:
    image_file = tmp_path / "photo.JPG"
    image_file.write_text("x")
    text_file = tmp_path / "notes.txt"
    text_file.write_text("x")

    assert is_supported_image(image_file)
    assert not is_supported_image(text_file)


def test_output_suffix_path(tmp_path: Path) -> None:
    source = tmp_path / "abc.jpeg"
    output = output_path_for(source, tmp_path / "out", "_framed")
    assert output.name == "abc_framed.jpeg"


def test_save_kwargs_jpeg_defaults_and_metadata() -> None:
    config = FrameConfig(
        input_dir=Path("."),
        output_dir=Path("."),
        frame_color="white",
        margin_top=100,
        margin_right=100,
        margin_bottom=100,
        margin_left=100,
        text="x",
    )
    kwargs = build_save_kwargs(".jpg", config, b"exif-bytes", b"icc-bytes")
    assert kwargs["quality"] == 90
    assert kwargs["exif"] == b"exif-bytes"
    assert kwargs["icc_profile"] == b"icc-bytes"


def test_save_kwargs_no_metadata_if_disabled() -> None:
    config = FrameConfig(
        input_dir=Path("."),
        output_dir=Path("."),
        frame_color="white",
        margin_top=100,
        margin_right=100,
        margin_bottom=100,
        margin_left=100,
        text="x",
        preserve_metadata=False,
    )
    kwargs = build_save_kwargs(".jpg", config, b"exif-bytes", b"icc-bytes")
    assert kwargs["quality"] == 90
    assert "exif" not in kwargs
    assert "icc_profile" not in kwargs

