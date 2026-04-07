from dataclasses import dataclass, field
from pathlib import Path
from typing import Any


@dataclass
class PdfInfo:
    path: Path
    pages: int
    is_image_only: bool
    metadata: dict[str, Any] = field(default_factory=dict)


@dataclass
class OcrPage:
    page_number: int
    text: str
    confidence: float | None = None
    artifacts: dict[str, Any] = field(default_factory=dict)


@dataclass
class ExtractionResult:
    template_id: str | None
    pdf: PdfInfo
    pages: list[OcrPage]
    parsed_rows: list[dict[str, Any]] = field(default_factory=list)
    warnings: list[str] = field(default_factory=list)
