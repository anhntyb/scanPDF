# Architecture

## Goal
Convert scanned Vietnamese PDF forms into Excel workbooks using a template-aware OCR pipeline.

## Pipeline

```text
Input PDF
  -> PDF inspection
  -> Page rasterization
  -> Image preprocessing
  -> OCR
  -> Template classification
  -> Region extraction / table parsing
  -> Data normalization
  -> Excel export
  -> Review artifacts
```

## Core modules

### 1. `scanner.pdf_inspector`
Reads metadata, page count, dimensions, and determines whether the PDF is image-based.

### 2. `scanner.rasterize`
Converts pages to PNG/JPEG images for downstream processing.

### 3. `scanner.preprocess`
Handles deskewing, thresholding, denoising, and contrast normalization.

### 4. `scanner.ocr`
Runs OCR against page images and returns text blocks with confidence.

### 5. `scanner.classify`
Maps a document to a known template family based on OCR text and layout features.

### 6. `scanner.extract`
Applies template-specific extraction rules:
- fixed fields by region
- repeated table areas
- page grouping

### 7. `scanner.normalize`
Cleans and standardizes values such as dates, IDs, names, and addresses.

### 8. `scanner.exporters.excel`
Creates workbook outputs:
- `summary`
- `raw_ocr`
- `parsed_data`
- `review_flags`

## Template strategy
Template definitions should live in `specs/templates/*.json` and describe:
- document id
- matching keywords
- expected pages
- regions of interest
- field names
- table definitions
- export mapping

## Review-first philosophy
OCR on scanned administrative documents will not be perfect. The system should track confidence and expose anything uncertain for human verification.
