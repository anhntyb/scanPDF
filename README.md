# ScanPDF

Desktop-oriented project for converting scanned PDF forms into structured Excel files.

## Current understanding

The sample files in `template/` are image-based scanned PDFs (HP Scan, ~200 DPI) with no embedded text layer. That means the correct extraction pipeline is:

1. Render PDF pages to images
2. Preprocess images (deskew, denoise, contrast, crop)
3. OCR Vietnamese text
4. Detect template/layout
5. Extract fields/tables using template rules
6. Normalize data
7. Export to Excel
8. Provide review hooks for low-confidence values

## Project layout

- `app/desktop` — desktop UI shell
- `app/worker` — OCR / extraction engine
- `specs/templates` — template definitions for known document families
- `docs` — architecture and roadmap
- `output` — generated files
- `scripts` — helper scripts
- `template` — sample input PDFs supplied by the user

## Development plan

### Phase 1 — MVP
- Detect known template family (`ca`, `cong_an`, `cong_an_tinh`, `scan_1`/unknown)
- Convert PDF to page images
- Produce OCR-ready artifacts
- Save OCR artifacts as JSON/text
- Export a basic Excel workbook with raw OCR and placeholder parsed rows

### Phase 2 — Structured extraction
- Add page/region extraction rules
- Add table segmentation and row parsing
- Add confidence scoring
- Add manual review support

### Phase 3 — Production usability
- Batch processing
- Template editor
- Error recovery workflow
- Packaging as desktop app

## Runtime recommendation

Use a Python worker for OCR and Excel generation. For the fastest Windows test path, the current project now also includes a lightweight Tkinter GUI that can be packaged into a `.exe` with PyInstaller.

## Next actions

1. Improve OCR row splitting and metadata cleanup
2. Ensure `tesseract` binary + Vietnamese language pack are installed on target Windows machines
3. Build `.exe` with PyInstaller on Windows
4. Add validation and review flags
5. Improve template-specific extraction rules
