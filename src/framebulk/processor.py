from __future__ import annotations

from pathlib import Path

from PIL import Image

from framebulk.image_ops import apply_frame_and_text, validate_config
from framebulk.models import BatchResult, FrameConfig

SUPPORTED_EXTENSIONS = {".jpg", ".jpeg", ".png", ".webp"}


def is_supported_image(path: Path) -> bool:
    return path.is_file() and path.suffix.lower() in SUPPORTED_EXTENSIONS


def output_path_for(source: Path, output_dir: Path, suffix: str) -> Path:
    return output_dir / f"{source.stem}{suffix}{source.suffix.lower()}"


def build_save_kwargs(
    suffix: str,
    config: FrameConfig,
    exif_bytes: bytes | None,
    icc_profile: bytes | None,
) -> dict[str, object]:
    kwargs: dict[str, object] = {}
    if suffix in {".jpg", ".jpeg"}:
        kwargs["quality"] = config.jpeg_quality

    if config.preserve_metadata:
        if exif_bytes:
            kwargs["exif"] = exif_bytes
        if icc_profile:
            kwargs["icc_profile"] = icc_profile
    return kwargs


def process_directory(config: FrameConfig) -> BatchResult:
    config = validate_config(config)
    if not config.input_dir.exists() or not config.input_dir.is_dir():
        raise ValueError(f"Input directory does not exist: {config.input_dir}")

    config.output_dir.mkdir(parents=True, exist_ok=True)

    processed = 0
    skipped = 0
    failed = 0

    for entry in sorted(config.input_dir.iterdir()):
        if not is_supported_image(entry):
            skipped += 1
            continue
        out_path = output_path_for(entry, config.output_dir, config.suffix)
        try:
            with Image.open(entry) as img:
                exif = img.info.get("exif")
                icc_profile = img.info.get("icc_profile")
                result = apply_frame_and_text(img, config)
            save_kwargs = build_save_kwargs(out_path.suffix.lower(), config, exif, icc_profile)
            result.save(out_path, **save_kwargs)
            processed += 1
            print(f"[ok] {entry.name} -> {out_path.name}")
        except Exception as exc:  # noqa: BLE001
            failed += 1
            print(f"[error] {entry.name}: {exc}")

    print(f"Done. processed={processed} failed={failed} skipped={skipped}")
    return BatchResult(processed=processed, failed=failed, skipped=skipped)

