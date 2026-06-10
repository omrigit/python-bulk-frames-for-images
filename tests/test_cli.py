from framebulk.cli import build_parser


def test_parse_apply_command() -> None:
    parser = build_parser()
    args = parser.parse_args(
        [
            "apply",
            "--input",
            "./images",
            "--output",
            "./out",
            "--frame-color",
            "white",
            "--text-align",
            "right",
            "--text-padding",
            "30",
            "--jpeg-quality",
            "92",
            "--no-preserve-metadata",
        ]
    )
    assert args.command == "apply"
    assert str(args.input) == "images"
    assert str(args.output) == "out"
    assert args.text_align == "right"
    assert args.text_padding == 30
    assert args.jpeg_quality == 92
    assert args.preserve_metadata is False


def test_parse_list_fonts_command() -> None:
    parser = build_parser()
    args = parser.parse_args(["list-fonts", "--contains", "arial", "--include-arabic"])
    assert args.command == "list-fonts"
    assert args.contains == "arial"
    assert args.include_arabic is True


def test_parse_color_cheatsheet_command() -> None:
    parser = build_parser()
    args = parser.parse_args(["color-cheatsheet", "--output", "./out/colors.jpg"])
    assert args.command == "color-cheatsheet"
    assert str(args.output) == "out/colors.jpg"


def test_parse_show_color_examples_without_command() -> None:
    parser = build_parser()
    args = parser.parse_args(["--show-color-examples"])
    assert args.show_color_examples is True
    assert args.command is None

