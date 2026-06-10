# Step-by-Step Instructions

This guide walks you through running `framebulk` with a concrete example:
- White frame
- Caption text: `this is a test let's go`
- Margins: `100px` on all sides

## 1) Open terminal in project folder

```bash
cd /Users/main/repositories-cursor/bulk-add-frames-to-images
```

## 2) Create and activate a virtual environment

```bash
python3 -m venv .venv
source .venv/bin/activate
```

## 3) Install dependencies

```bash
PIP_INDEX_URL=https://pypi.org/simple pip install Pillow pytest
```

## 4) Prepare input images

Create an `images` folder in the project root and copy your source images into it.

Expected input folder:
- `./images`

Output folder that will be created:
- `./out`

## 5) Run the exact example command

```bash
PYTHONPATH=src python -m framebulk.cli apply \
  --input ./images \
  --output ./out \
  --frame-color white \
  --margin-top 100 \
  --margin-right 100 \
  --margin-bottom 100 \
  --margin-left 100 \
  --text "this is a test let's go" \
  --font-family Arial \
  --font-size 48 \
  --text-color black \
  --text-position auto \
  --text-align center \
  --text-padding 40 \
  --jpeg-quality 90 \
  --preserve-metadata
```

## 6) Check results

Processed files are saved to `./out` with `_framed` added to their filenames.

Example:
- `photo.jpg` -> `photo_framed.jpg`

## Helpful commands

Show all CLI options:

```bash
PYTHONPATH=src python -m framebulk.cli --help
```

Text is always rendered on the bottom frame surface only (for portrait and landscape).
`--text-position` is accepted for compatibility but currently ignored by design.
`--text-padding` controls inner safe space from frame corners/edges (default `40`).
`--jpeg-quality` defaults to `90` for JPEG output.
`--preserve-metadata` is enabled by default (use `--no-preserve-metadata` to disable).
The CLI now validates colors/fonts before processing and prints actionable error messages for typos.

List available fonts:

```bash
PYTHONPATH=src python -m framebulk.cli list-fonts
```

Arabic-only fonts are excluded by default. To include them:

```bash
PYTHONPATH=src python -m framebulk.cli list-fonts --include-arabic
```

Filter and see bundled fonts quickly:

```bash
PYTHONPATH=src python -m framebulk.cli list-fonts --contains variable
```

Bundled fonts included in this project:
- `Lato-Regular`
- `Lato-Bold`
- `Montserrat-Variable`
- `Nunito-Variable`
- `Oswald-Variable`
- `Raleway-Variable`
- `Alef-Regular` (Hebrew)
- `Alef-Bold` (Hebrew)
- `Assistant-Variable` (Hebrew support)
- `Heebo-Variable` (Hebrew support)

Show color examples:

```bash
PYTHONPATH=src python -m framebulk.cli --show-color-examples
```

Generate a visual font cheat sheet PNG:

```bash
PYTHONPATH=src python scripts/generate_font_cheatsheet.py
```

Output file:
- `./out/font-cheatsheet.png`

Generate a JPG with all available named colors (great for choosing frame/text colors):

```bash
PYTHONPATH=src python -m framebulk.cli color-cheatsheet --output ./out/color-cheatsheet.jpg
```

Output file:
- `./out/color-cheatsheet.jpg`

Pick a text position/alignment manually:

```bash
PYTHONPATH=src python -m framebulk.cli apply \
  --input ./images \
  --output ./out \
  --frame-color white \
  --margin-top 100 \
  --margin-right 100 \
  --margin-bottom 100 \
  --margin-left 100 \
  --text "this is a test let's go" \
  --font-family Arial \
  --font-size 48 \
  --text-color black \
  --text-position top \
  --text-align right
```

## Full command reference (copy/paste)

Activate environment (once per terminal session):

```bash
cd /Users/main/repositories-cursor/bulk-add-frames-to-images
source .venv/bin/activate
```

Show global help:

```bash
PYTHONPATH=src python -m framebulk.cli --help
```

Show color examples:

```bash
PYTHONPATH=src python -m framebulk.cli --show-color-examples
```

List all fonts:

```bash
PYTHONPATH=src python -m framebulk.cli list-fonts
```

Filter fonts:

```bash
PYTHONPATH=src python -m framebulk.cli list-fonts --contains comic
```

Generate font cheat sheet PNG:

```bash
PYTHONPATH=src python scripts/generate_font_cheatsheet.py
```

Generate all named colors cheat sheet JPG:

```bash
PYTHONPATH=src python -m framebulk.cli color-cheatsheet --output ./out/color-cheatsheet.jpg
```

Apply frames with all major flags (default settings shown explicitly):

```bash
PYTHONPATH=src python -m framebulk.cli apply \
  --input /Users/main/BULK-FRAME-TRIES/001 \
  --output /Users/main/BULK-FRAME-TRIES/001/out \
  --frame-color white \
  --margin-top 200 \
  --margin-right 200 \
  --margin-bottom 400 \
  --margin-left 200 \
  --text "This is a test let's go" \
  --text-position auto \
  --text-align center \
  --font-family "Comic Sans MS Bold" \
  --font-size 50 \
  --min-font-size 12 \
  --text-color black \
  --jpeg-quality 90 \
  --preserve-metadata \
  --suffix _framed
```

Same command with metadata disabled:

```bash
PYTHONPATH=src python -m framebulk.cli apply \
  --input /Users/main/BULK-FRAME-TRIES/001 \
  --output /Users/main/BULK-FRAME-TRIES/001/out_no_meta \
  --frame-color white \
  --margin-top 200 \
  --margin-right 200 \
  --margin-bottom 400 \
  --margin-left 200 \
  --text "This is a test let's go" \
  --text-position auto \
  --text-align center \
  --font-family "Comic Sans MS Bold" \
  --font-size 50 \
  --min-font-size 12 \
  --text-color black \
  --jpeg-quality 90 \
  --no-preserve-metadata \
  --suffix _framed
```
