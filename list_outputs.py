from pathlib import Path

root = Path(__file__).resolve().parent / "output"
for path in sorted(root.rglob("*")):
    if path.is_file():
        print(path.relative_to(root.parent))
