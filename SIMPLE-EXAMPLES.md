# Simple Command Examples

This page is intentionally high-level and easy to copy/paste.

## Before you run commands

Open terminal in the project folder and activate the virtual environment:

```bash
cd /Users/main/repositories-cursor/bulk-add-frames-to-images
source .venv/bin/activate
```

All examples below use:
- input folder: `/Users/main/BULK-FRAME-TRIES/001`
- output folder: different per example

---

## 1) Full example with all major flags (white borders)

```bash
PYTHONPATH=src python -m framebulk.cli apply \
  --input /Users/main/BULK-FRAME-TRIES/001 \
  --output /Users/main/BULK-FRAME-TRIES/001/out_example_1 \
  --frame-color white \
  --margin-top 200 \
  --margin-right 200 \
  --margin-bottom 400 \
  --margin-left 200 \
  --text "This is a test let's go" \
  --text-position auto \
  --text-align center \
  --text-padding 40 \
  --font-family "Comic Sans MS Bold" \
  --font-size 50 \
  --min-font-size 12 \
  --text-color black \
  --jpeg-quality 90 \
  --preserve-metadata \
  --suffix _framed
```

---

## 2) Different style: black borders + gold text + different font

```bash
PYTHONPATH=src python -m framebulk.cli apply \
  --input /Users/main/BULK-FRAME-TRIES/001 \
  --output /Users/main/BULK-FRAME-TRIES/001/out_example_2 \
  --frame-color black \
  --margin-top 160 \
  --margin-right 160 \
  --margin-bottom 260 \
  --margin-left 160 \
  --text "Friday vibes" \
  --text-position bottom \
  --text-align right \
  --text-padding 60 \
  --font-family "Montserrat-Variable" \
  --font-size 44 \
  --min-font-size 12 \
  --text-color gold \
  --jpeg-quality 90 \
  --preserve-metadata \
  --suffix _styled
```

---

## 3) Clean minimal style (small frame, no custom text color)

```bash
PYTHONPATH=src python -m framebulk.cli apply \
  --input /Users/main/BULK-FRAME-TRIES/001 \
  --output /Users/main/BULK-FRAME-TRIES/001/out_example_3 \
  --frame-color white \
  --margin-top 80 \
  --margin-right 80 \
  --margin-bottom 120 \
  --margin-left 80 \
  --text "Minimal look" \
  --text-position auto \
  --text-align center \
  --text-padding 30 \
  --font-family "Lato-Regular" \
  --font-size 34 \
  --min-font-size 12 \
  --jpeg-quality 90 \
  --preserve-metadata \
  --suffix _minimal
```

---

## 4) Hebrew-friendly example

```bash
PYTHONPATH=src python -m framebulk.cli apply \
  --input /Users/main/BULK-FRAME-TRIES/001 \
  --output /Users/main/BULK-FRAME-TRIES/001/out_example_4 \
  --frame-color white \
  --margin-top 120 \
  --margin-right 120 \
  --margin-bottom 220 \
  --margin-left 120 \
  --text "זה טקסט לדוגמה" \
  --text-position bottom \
  --text-align center \
  --text-padding 40 \
  --font-family "Alef-Bold" \
  --font-size 46 \
  --min-font-size 14 \
  --text-color navy \
  --jpeg-quality 90 \
  --preserve-metadata \
  --suffix _he
```

---

## 5) Same idea, but with metadata disabled

```bash
PYTHONPATH=src python -m framebulk.cli apply \
  --input /Users/main/BULK-FRAME-TRIES/001 \
  --output /Users/main/BULK-FRAME-TRIES/001/out_example_5 \
  --frame-color white \
  --margin-top 180 \
  --margin-right 180 \
  --margin-bottom 320 \
  --margin-left 180 \
  --text "No metadata version" \
  --text-position auto \
  --text-align left \
  --text-padding 40 \
  --font-family "Assistant-Variable" \
  --font-size 42 \
  --min-font-size 12 \
  --text-color black \
  --jpeg-quality 90 \
  --no-preserve-metadata \
  --suffix _no_meta
```

