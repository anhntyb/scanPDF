from __future__ import annotations

from pathlib import Path

import fitz


def rasterize_pdf(path: str | Path, output_dir: str | Path, dpi: int = 200, limit_pages: int | None = None) -> list[Path]:
    pdf_path = Path(path)
    out_dir = Path(output_dir)
    out_dir.mkdir(parents=True, exist_ok=True)

    doc = fitz.open(pdf_path)
    scale = dpi / 72.0
    matrix = fitz.Matrix(scale, scale)

    image_paths: list[Path] = []
    total = len(doc)
    page_count = min(total, limit_pages) if limit_pages else total

    for index in range(page_count):
        page = doc.load_page(index)
        pix = page.get_pixmap(matrix=matrix, alpha=False)
        image_path = out_dir / f"page-{index + 1:03d}.png"
        pix.save(str(image_path))
        image_paths.append(image_path)

    return image_paths
