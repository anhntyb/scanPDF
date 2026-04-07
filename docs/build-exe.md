# Build Windows EXE

## Mục tiêu
Đóng gói ScanPDF thành app Windows `.exe` bằng PyInstaller.

## Chuẩn bị trên Windows
- Cài Python 3.12+
- Cài Tesseract OCR cho Windows
- Thêm `tesseract.exe` vào PATH
- Nếu dùng tiếng Việt, cài language data `vie`

## Build nhanh
Trong thư mục project:

### CMD
```bat
build_windows.bat
```

### PowerShell
```powershell
.\build_windows.ps1
```

## File đầu ra
```text
dist\ScanPDF\ScanPDF.exe
```

## Nếu app mở được nhưng OCR không chạy
Kiểm tra:
```bat
tesseract --version
```

Nếu không ra version thì PATH chưa đúng.

## Tính năng GUI hiện tại
- Chọn file PDF
- Chọn file Excel đầu ra
- Chọn số trang chạy thử
- Bấm `Chạy`
- Xem log ngay trong app

## Ghi chú
Bản GUI hiện tại là MVP để test flow nội bộ. Chưa có drag/drop, preview trang, hay màn hình sửa lỗi OCR.
