#!/usr/bin/env bash
set -euo pipefail

cd "$(dirname "$0")/.."
source .venv/bin/activate

python app/worker/main.py inspect template/ca.pdf
python app/worker/main.py export template/ca.pdf --output output/generated/ca-output.xlsx
python app/worker/main.py process template/ca.pdf --work-root output/artifacts --output output/generated/ca-processed.xlsx --limit-pages 2

echo "Sample run complete"
