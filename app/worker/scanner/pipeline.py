from __future__ import annotations

import json
from pathlib import Path

from .classify import classify_document
from .export_excel import export_result
from .models import ExtractionResult
from .ocr import is_tesseract_available, run_ocr
from .parse_rows import parse_rows_from_pages
from .pdf_inspector import inspect_pdf
from .preprocess import preprocess_image
from .rasterize import rasterize_pdf


def process_pdf(
    pdf_path: str | Path,
    work_root: str | Path,
    output_xlsx: str | Path | None = None,
    limit_pages: int | None = None,
) -> ExtractionResult:
    pdf_path = Path(pdf_path)
    work_root = Path(work_root)
    stem = pdf_path.stem

    raster_dir = work_root / "rasterized" / stem
    prep_dir = work_root / "preprocessed" / stem
    ocr_dir = work_root / "ocr" / stem
    ocr_dir.mkdir(parents=True, exist_ok=True)

    pdf_info = inspect_pdf(pdf_path)
    rasterized = rasterize_pdf(pdf_path, raster_dir, dpi=200, limit_pages=limit_pages)

    pages = []
    for i, image_path in enumerate(rasterized, start=1):
        processed_path = prep_dir / image_path.name
        preprocess_image(image_path, processed_path)
        page = run_ocr(processed_path, page_number=i)
        pages.append(page)

    combined_text = "\n".join(page.text for page in pages if page.text)
    template_id = classify_document(pdf_path, combined_text)

    parsed_rows, parse_warnings, metadata = parse_rows_from_pages(pages, template_id, pdf_path.name)

    result = ExtractionResult(
        template_id=template_id,
        pdf=pdf_info,
        pages=pages,
        parsed_rows=parsed_rows,
        warnings=parse_warnings,
    )

    if not is_tesseract_available():
        result.warnings.append("Tesseract binary is not installed; OCR text is empty")

    json_path = ocr_dir / "raw_ocr.json"
    text_path = ocr_dir / "raw_ocr.txt"
    json_payload = {
        "template_id": template_id,
        "pdf": str(pdf_path),
        "metadata": metadata,
        "pages": [
            {
                "page_number": p.page_number,
                "confidence": p.confidence,
                "text": p.text,
                "artifacts": p.artifacts,
            }
            for p in pages
        ],
        "parsed_rows": parsed_rows,
        "warnings": result.warnings,
    }
    json_path.write_text(json.dumps(json_payload, ensure_ascii=False, indent=2), encoding="utf-8")
    text_path.write_text("\n\n".join([f"--- PAGE {p.page_number} ---\n{p.text}" for p in pages]), encoding="utf-8")

    if output_xlsx:
        export_result(result, output_xlsx)

    return result
