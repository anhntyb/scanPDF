from __future__ import annotations

import subprocess
from pathlib import Path

from .models import PdfInfo


def inspect_pdf(path: str | Path) -> PdfInfo:
    pdf_path = Path(path)
    result = subprocess.run(["pdfinfo", str(pdf_path)], capture_output=True, text=True, check=True)
    output = result.stdout.splitlines()

    metadata: dict[str, str] = {}
    pages = 0
    for line in output:
        if ":" not in line:
            continue
        key, value = line.split(":", 1)
        metadata[key.strip()] = value.strip()
        if key.strip() == "Pages":
            try:
                pages = int(value.strip())
            except ValueError:
                pages = 0

    image_only = True
    try:
        img_result = subprocess.run(["pdfimages", "-list", str(pdf_path)], capture_output=True, text=True, check=True)
        image_only = "image" in img_result.stdout.lower()
    except Exception:
        image_only = True

    return PdfInfo(path=pdf_path, pages=pages, is_image_only=image_only, metadata=metadata)
