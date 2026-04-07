from __future__ import annotations

import re
from typing import Any

from .models import OcrPage

AMOUNT_PATTERN = re.compile(r"\b\d{1,3}(?:[\.,]\d{3})+(?:[\.,]\d+)?\b|\b\d{6,}\b")
ACCOUNT_PATTERN = re.compile(r"\b\d{9,16}\b")
ROW_PATTERN = re.compile(r"^\s*(\d{1,3})\s+")
CODE_PATTERN = re.compile(r"\b10\d{5,8}\b")
MONTH_YEAR_PATTERN = re.compile(r"THANG\s+(\d{1,2})\s*/\s*(\d{4})|THÁNG\s+(\d{1,2})\s*/\s*(\d{4})", re.IGNORECASE)


def normalize_amount(value: str | None) -> int | None:
    if not value:
        return None
    digits = re.sub(r"\D", "", value)
    if not digits:
        return None
    try:
        return int(digits)
    except ValueError:
        return None


def extract_document_metadata(text: str) -> dict[str, Any]:
    upper = text.upper()
    month = None
    year = None
    m = MONTH_YEAR_PATTERN.search(text)
    if m:
        month = next((g for g in [m.group(1), m.group(3)] if g), None)
        year = next((g for g in [m.group(2), m.group(4)] if g), None)

    unit_name = None
    for line in text.splitlines()[:8]:
        if "Công an tỉnh" in line or "CÔNG AN TỈNH" in line:
            unit_name = line.strip()
            break

    title = None
    for line in text.splitlines()[:12]:
        stripped = line.strip()
        if len(stripped) > 12 and ("DANH SÁCH" in stripped.upper() or "BANG KE" in stripped.upper() or "BẢNG KÊ" in stripped.upper()):
            title = stripped
            break

    bank_name = None
    if "Agribank" in text:
        bank_name = "Agribank"

    return {
        "unit_name": unit_name,
        "title": title,
        "month": month,
        "year": year,
        "bank_name": bank_name,
    }


def parse_line_to_row(line: str, template_id: str | None, page_number: int, source_file: str, metadata: dict[str, Any]) -> dict[str, Any] | None:
    compact = " ".join(line.split())
    if not compact:
        return None
    if any(keyword in compact.lower() for keyword in ["tổng cộng", "nguời lập", "người lập", "kế toán", "thủ trưởng", "đại tá"]):
        return None

    row_match = ROW_PATTERN.match(compact)
    account_match = ACCOUNT_PATTERN.search(compact)
    amount_matches = AMOUNT_PATTERN.findall(compact)

    if not row_match or not account_match or not amount_matches:
        return None

    row_no = row_match.group(1)
    account = account_match.group(0)
    amount = normalize_amount(amount_matches[-1])

    code_match = CODE_PATTERN.search(compact)
    code = code_match.group(0) if code_match else None

    start = row_match.end()
    end = account_match.start()
    middle = compact[start:end].strip(" |_-—[]")
    if code and middle.startswith(code):
        middle = middle[len(code):].strip(" |_-—[]")

    full_name = re.sub(r"\s{2,}", " ", middle).strip()
    if len(full_name) < 2:
        return None

    return {
        "source_file": source_file,
        "template_id": template_id or "unknown",
        "page_number": page_number,
        "row_no": row_no,
        "code": code,
        "full_name": full_name,
        "bank_account": account,
        "amount": amount,
        "currency": "VND",
        "unit_name": metadata.get("unit_name"),
        "title": metadata.get("title"),
        "month": metadata.get("month"),
        "year": metadata.get("year"),
        "bank_name": metadata.get("bank_name"),
        "raw_line": compact,
    }


def parse_rows_from_pages(pages: list[OcrPage], template_id: str | None, source_file: str) -> tuple[list[dict[str, Any]], list[str], dict[str, Any]]:
    all_text = "\n".join(page.text for page in pages)
    metadata = extract_document_metadata(all_text)
    rows: list[dict[str, Any]] = []
    warnings: list[str] = []

    for page in pages:
        candidates = re.split(r"(?<=\D)\|\s*(?=\d{1,3}\s)|\n", page.text)
        matched = 0
        for line in candidates:
            row = parse_line_to_row(line, template_id, page.page_number, source_file, metadata)
            if row:
                rows.append(row)
                matched += 1
        if matched == 0:
            warnings.append(f"No structured rows parsed on page {page.page_number}")

    return rows, warnings, metadata
