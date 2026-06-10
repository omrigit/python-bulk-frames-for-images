from __future__ import annotations

import argparse
from pathlib import Path

from framebulk.color_sheet import generate_color_cheatsheet
from framebulk.fonts import list_system_fonts
from framebulk.models import FrameConfig
from framebulk.processor import process_directory


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="framebulk",
        description="Bulk add frames and captions to images.",
        formatter_class=argparse.RawTextHelpFormatter,
        epilog=(
            "Examples:\n"
            "  framebulk --show-color-examples\n"
            "  framebulk list-fonts\n"
            "  framebulk list-fonts --contains arial\n"
            "  framebulk apply --input ./images --output ./out --frame-color white \\\n"
            "    --margin-top 60 --margin-right 60 --margin-bottom 140 --margin-left 60 \\\n"
            "    --text \"Shabbat Shalom\" --font-family Arial --font-size 48 \\\n"
            "    --text-position top --text-align center --text-padding 40 --jpeg-quality 90 --preserve-metadata\n"
            "  framebulk color-cheatsheet --output ./out/color-cheatsheet.jpg\n\n"
            "Color values support names (white, black, red) and hex (#RRGGBB).\n"
            "When --text-color is omitted, contrast defaults are used based on frame color."
        ),
    )
    parser.add_argument(
        "--show-color-examples",
        action="store_true",
        help="Print valid text/frame color examples (names and hex formats).",
    )
    subparsers = parser.add_subparsers(dest="command", required=False)

    apply_parser = subparsers.add_parser("apply", help="Apply frames to all images in a folder.")
    apply_parser.add_argument("--input", required=True, type=Path, help="Input directory path with source images")
    apply_parser.add_argument("--output", required=True, type=Path, help="Output directory path for framed images")
    apply_parser.add_argument(
        "--frame-color",
        required=True,
        help="Frame color (e.g. white, black, #RRGGBB)",
    )
    apply_parser.add_argument("--margin-top", type=int, default=60, help="Top frame margin in pixels")
    apply_parser.add_argument("--margin-right", type=int, default=60, help="Right frame margin in pixels")
    apply_parser.add_argument("--margin-bottom", type=int, default=120, help="Bottom frame margin in pixels")
    apply_parser.add_argument("--margin-left", type=int, default=60, help="Left frame margin in pixels")
    apply_parser.add_argument("--text", default="", help="Caption text to place on frame")
    apply_parser.add_argument(
        "--text-position",
        choices=["auto", "top", "bottom", "left", "right"],
        default="auto",
        help="Compatibility flag (text is currently always placed on bottom frame).",
    )
    apply_parser.add_argument(
        "--text-align",
        choices=["left", "center", "right"],
        default="center",
        help="Text alignment inside chosen frame side.",
    )
    apply_parser.add_argument(
        "--font-family",
        default=None,
        help="Font family name (use 'framebulk list-fonts' to discover choices)",
    )
    apply_parser.add_argument("--font-path", type=Path, default=None, help="Path to specific .ttf/.otf/.ttc font file")
    apply_parser.add_argument("--font-size", type=int, default=48, help="Starting font size in pixels")
    apply_parser.add_argument("--min-font-size", type=int, default=12, help="Minimum font size when auto-shrinking")
    apply_parser.add_argument(
        "--text-color",
        default=None,
        help="Text color (name or hex). Omit to auto-pick contrast.",
    )
    apply_parser.add_argument(
        "--text-padding",
        type=int,
        default=40,
        help="Inner padding in pixels inside bottom frame (default: 40).",
    )
    apply_parser.add_argument(
        "--jpeg-quality",
        type=int,
        default=90,
        help="JPEG output quality 1-100 (default: 90).",
    )
    apply_parser.add_argument(
        "--preserve-metadata",
        action=argparse.BooleanOptionalAction,
        default=True,
        help="Preserve metadata like EXIF and ICC profile (default: enabled).",
    )
    apply_parser.add_argument("--suffix", default="_framed", help="Suffix for generated files")

    fonts_parser = subparsers.add_parser("list-fonts", help="List available system font names.")
    fonts_parser.add_argument(
        "--contains",
        default=None,
        help="Filter font names by substring (case-insensitive).",
    )
    fonts_parser.add_argument(
        "--include-arabic",
        action="store_true",
        help="Include Arabic-only fonts in listing (excluded by default).",
    )

    colors_parser = subparsers.add_parser(
        "color-cheatsheet",
        help="Generate a JPG file showing all named colors available in Pillow.",
    )
    colors_parser.add_argument(
        "--output",
        type=Path,
        default=Path("out/color-cheatsheet.jpg"),
        help="Output JPG path for color cheatsheet.",
    )
    return parser


def print_color_examples() -> None:
    print("Color examples you can use with --frame-color / --text-color:")
    print("  Named colors: white, black, red, blue, navy, gold, orange, purple, gray")
    print("  Hex colors:   #FFFFFF, #000000, #FF5733, #1E90FF")
    print("  Tip: Pillow accepts many CSS-style color names (case-insensitive).")


def main() -> None:
    parser = build_parser()
    args = parser.parse_args()

    if args.show_color_examples:
        print_color_examples()
        return

    if args.command == "list-fonts":
        query = (args.contains or "").strip().lower()
        fonts = list_system_fonts(include_arabic=args.include_arabic)
        if query:
            fonts = [item for item in fonts if query in item[0].lower()]
        if not fonts:
            print("No matching fonts found.")
            return
        for name, path in fonts:
            print(f"{name}\t{path}")
        return

    if args.command == "color-cheatsheet":
        output = generate_color_cheatsheet(args.output)
        print(f"Created {output}")
        return

    if args.command != "apply":
        parser.print_help()
        return

    config = FrameConfig(
        input_dir=args.input,
        output_dir=args.output,
        frame_color=args.frame_color,
        margin_top=args.margin_top,
        margin_right=args.margin_right,
        margin_bottom=args.margin_bottom,
        margin_left=args.margin_left,
        text=args.text,
        text_position=args.text_position,
        text_align=args.text_align,
        font_family=args.font_family,
        font_path=args.font_path,
        font_size=args.font_size,
        min_font_size=args.min_font_size,
        text_color=args.text_color,
        text_padding=args.text_padding,
        jpeg_quality=args.jpeg_quality,
        preserve_metadata=args.preserve_metadata,
        suffix=args.suffix,
    )
    try:
        process_directory(config)
    except ValueError as exc:
        parser.exit(status=2, message=f"Error: {exc}\n")


if __name__ == "__main__":
    main()

