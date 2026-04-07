from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parent
sys.path.insert(0, str(ROOT / "app" / "worker"))

from main import command_process  # noqa: E402


def main() -> int:
    jobs = [
        (ROOT / "template" / "Scan-1.pdf", ROOT / "output" / "artifacts", ROOT / "output" / "generated" / "scan-1.xlsx", 2),
        (ROOT / "template" / "ca.pdf", ROOT / "output" / "artifacts", ROOT / "output" / "generated" / "ca-processed.xlsx", 2),
    ]
    for pdf, work_root, output, limit_pages in jobs:
        print(f"=== Processing {pdf.name} ===")
        command_process(str(pdf), str(work_root), str(output), limit_pages)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
