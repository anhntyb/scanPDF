from __future__ import annotations

import argparse
from pathlib import Path

from scanner.classify import classify_document
from scanner.export_excel import export_result
from scanner.models import ExtractionResult
from scanner.pdf_inspector import inspect_pdf
from scanner.pipeline import process_pdf


def build_arg_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="ScanPDF worker")
    sub = parser.add_subparsers(dest="command", required=True)

    inspect_cmd = sub.add_parser("inspect", help="Inspect a PDF")
    inspect_cmd.add_argument("pdf")

    export_cmd = sub.add_parser("export", help="Inspect and export placeholder Excel")
    export_cmd.add_argument("pdf")
    export_cmd.add_argument("--output", required=True)

    process_cmd = sub.add_parser("process", help="Run rasterize/preprocess/OCR pipeline")
    process_cmd.add_argument("pdf")
    process_cmd.add_argument("--work-root", default="output/artifacts")
    process_cmd.add_argument("--output")
    process_cmd.add_argument("--limit-pages", type=int)

    return parser


def command_inspect(pdf: str) -> int:
    info = inspect_pdf(pdf)
    print(f"PDF: {info.path}")
    print(f"Pages: {info.pages}")
    print(f"Image-only scan: {info.is_image_only}")
    for key, value in info.metadata.items():
        print(f"{key}: {value}")
    return 0


def command_export(pdf: str, output: str) -> int:
    info = inspect_pdf(pdf)
    template_id = classify_document(pdf)
    result = ExtractionResult(
        template_id=template_id,
        pdf=info,
        pages=[],
        parsed_rows=[],
        warnings=[
            "OCR/extraction not implemented yet",
            "This workbook is a scaffold output",
        ],
    )
    out = export_result(result, output)
    print(f"Exported: {out}")
    return 0


def command_process(pdf: str, work_root: str, output: str | None, limit_pages: int | None) -> int:
    result = process_pdf(pdf, work_root=work_root, output_xlsx=output, limit_pages=limit_pages)
    print(f"Processed: {result.pdf.path}")
    print(f"Template: {result.template_id or 'unknown'}")
    print(f"Pages: {len(result.pages)}")
    for warning in result.warnings:
        print(f"Warning: {warning}")
    return 0


def main() -> int:
    parser = build_arg_parser()
    args = parser.parse_args()

    if args.command == "inspect":
        return command_inspect(args.pdf)
    if args.command == "export":
        return command_export(args.pdf, args.output)
    if args.command == "process":
        return command_process(args.pdf, args.work_root, args.output, args.limit_pages)
    parser.error("Unknown command")
    return 2


if __name__ == "__main__":
    raise SystemExit(main())
