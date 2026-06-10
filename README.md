# framebulk

CLI tool to bulk add frames and caption text to images with orientation-aware layout.

Step-by-step walkthrough: see `INSTRUCTIONS.md`.
Complete copy/paste command reference (all flags + commands): see `INSTRUCTIONS.md` section `Full command reference (copy/paste)`.

## Install

```bash
python -m venv .venv
source .venv/bin/activate
pip install -e ".[dev]"
```

## Usage

```bash
framebulk apply \
  --input ./images \
  --output ./out \
  --frame-color white \
  --margin-top 60 \
  --margin-right 60 \
  --margin-bottom 140 \
  --margin-left 60 \
  --text "Sample caption" \
  --font-family Arial \
  --font-size 48 \
  --text-color black \
  --text-position auto \
  --text-align center \
  --text-padding 40 \
  --jpeg-quality 90 \
  --preserve-metadata
```

### Notes

- Text is always rendered on the bottom frame only (never on the image itself).
- `--text-position` is accepted for compatibility but currently ignored by design.
- `--text-align` controls placement inside the selected side (`left`, `center`, `right`).
- `--text-padding` keeps space from frame corners/edges (default `40`).
- If `--text-color` is omitted, contrast defaults are used:
  - white frame -> black text
  - black frame -> white text
- `--jpeg-quality` controls JPEG save quality (default `90`).
- `--preserve-metadata` is enabled by default and keeps EXIF/ICC when available (disable with `--no-preserve-metadata`).
- Colors and fonts are validated before processing starts, with typo suggestions in error messages.
- You can pass `--font-path` to force a specific font file.
- Use `framebulk list-fonts --contains <query>` to discover valid font names.
- Arabic-only fonts are excluded by default from `list-fonts` and the font cheatsheet (use `framebulk list-fonts --include-arabic` if needed).
- Bundled extra fonts are included in `assets/fonts` (for example `Lato-Regular`, `Montserrat-Variable`, `Nunito-Variable`, `Oswald-Variable`, `Raleway-Variable`, `Alef-Regular`, `Alef-Bold`, `Assistant-Variable`, `Heebo-Variable`).
- Generate a visual preview of fonts with `PYTHONPATH=src python scripts/generate_font_cheatsheet.py` (output: `out/font-cheatsheet.png`).
- Generate a JPG with all available named colors: `PYTHONPATH=src python -m framebulk.cli color-cheatsheet --output out/color-cheatsheet.jpg`.
