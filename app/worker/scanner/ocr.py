from __future__ import annotations

import shutil
from pathlib import Path

import pytesseract
from PIL import Image

from .models import OcrPage


def is_tesseract_available() -> bool:
    return shutil.which("tesseract") is not None


def run_ocr(image_path: str | Path, page_number: int, lang: str = "vie+eng") -> OcrPage:
    image = Image.open(image_path)
    if not is_tesseract_available():
        return OcrPage(
            page_number=page_number,
            text="",
            confidence=None,
            artifacts={
                "status": "tesseract_missing",
                "image_path": str(image_path),
                "lang": lang,
            },
        )

    data = pytesseract.image_to_data(
        image,
        lang=lang,
        output_type=pytesseract.Output.DICT,
        config="--oem 3 --psm 6",
    )

    words = []
    confidences = []
    for text, conf in zip(data.get("text", []), data.get("conf", [])):
        if not text or not str(text).strip():
            continue
        try:
            conf_value = float(conf)
        except Exception:
            conf_value = -1
        if conf_value >= 0:
            words.append(text)
            confidences.append(conf_value)

    confidence = round(sum(confidences) / len(confidences), 2) if confidences else None
    return OcrPage(
        page_number=page_number,
        text=" ".join(words),
        confidence=confidence,
        artifacts={
            "image_path": str(image_path),
            "word_count": len(words),
        },
    )
