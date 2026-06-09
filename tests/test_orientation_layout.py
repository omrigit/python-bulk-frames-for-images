from framebulk.image_ops import classify_orientation, resolve_text_position, text_region


def test_orientation_portrait() -> None:
    assert classify_orientation(1080, 1920) == "portrait"


def test_orientation_landscape() -> None:
    assert classify_orientation(1920, 1080) == "landscape"


def test_auto_position_portrait() -> None:
    assert resolve_text_position("auto", "portrait") == "auto"


def test_auto_position_landscape() -> None:
    assert resolve_text_position("auto", "landscape") == "auto"


def test_text_region_fallback_when_requested_margin_is_zero() -> None:
    x, y, w, h, resolved = text_region(
        out_w=1200,
        out_h=1800,
        image_w=1000,
        image_h=1600,
        margin_top=0,
        margin_right=100,
        margin_bottom=100,
        margin_left=100,
        requested_position="top",
        orientation="portrait",
    )
    assert (x, y, w, h) == (100, 1600, 1000, 100)
    assert resolved == "bottom"


def test_text_region_auto_prefers_largest_available_margin() -> None:
    x, y, w, h, resolved = text_region(
        out_w=1300,
        out_h=1700,
        image_w=900,
        image_h=1200,
        margin_top=200,
        margin_right=200,
        margin_bottom=400,
        margin_left=200,
        requested_position="auto",
        orientation="landscape",
    )
    assert (x, y, w, h) == (200, 1400, 900, 400)
    assert resolved == "bottom"

