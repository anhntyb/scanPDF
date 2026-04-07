from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parent
sys.path.insert(0, str(ROOT / "app" / "worker"))

from main import command_process  # noqa: E402


def main() -> int:
    template_dir = ROOT / "template"
    outputs = ROOT / "output"
    for pdf in sorted(template_dir.glob("*.pdf")):
        stem = pdf.stem.replace(" ", "-").lower()
        print(f"=== Processing {pdf.name} ===")
        command_process(str(pdf), str(outputs / "artifacts"), str(outputs / "generated" / f"{stem}.xlsx"), 3)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
