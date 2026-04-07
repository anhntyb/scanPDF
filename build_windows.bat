@echo off
setlocal
cd /d %~dp0

if not exist .venv (
  py -m venv .venv
)

call .venv\Scripts\activate.bat
python -m pip install --upgrade pip
pip install -r requirements-build.txt

pyinstaller ^
  --noconfirm ^
  --clean ^
  --windowed ^
  --name ScanPDF ^
  --paths app\worker ^
  --add-data "template;template" ^
  --add-data "specs;specs" ^
  --add-data "README.md;." ^
  app\gui\app.py

echo.
echo Build xong. File exe nam o: dist\ScanPDF\ScanPDF.exe
pause
