Set-Location $PSScriptRoot

if (-not (Test-Path .venv)) {
    py -m venv .venv
}

& .\.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
pip install -r requirements-build.txt

pyinstaller \
  --noconfirm \
  --clean \
  --windowed \
  --name ScanPDF \
  --paths app\worker \
  --add-data "template;template" \
  --add-data "specs;specs" \
  --add-data "README.md;." \
  app\gui\app.py

Write-Host "`nBuild xong. File exe nam o: dist\ScanPDF\ScanPDF.exe"
