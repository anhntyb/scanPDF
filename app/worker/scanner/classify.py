from __future__ import annotations

from pathlib import Path


def classify_document(path: str | Path, ocr_text: str = "") -> str | None:
    name = Path(path).name.lower()
    if "cong an tinh" in name:
        return "cong_an_tinh"
    if "cong an" in name:
        return "cong_an"
    if name.startswith("ca") or name == "ca.pdf":
        return "ca"

    text = ocr_text.lower()
    if "công an tỉnh" in text:
        return "cong_an_tinh"
    if "công an" in text:
        return "cong_an"
    return None
