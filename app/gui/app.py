from __future__ import annotations

import sys
import threading
from pathlib import Path
import tkinter as tk
from tkinter import filedialog, messagebox, ttk

ROOT = Path(__file__).resolve().parents[2]
WORKER_ROOT = ROOT / "app" / "worker"
sys.path.insert(0, str(WORKER_ROOT))

from scanner.pipeline import process_pdf  # noqa: E402


class ScanPdfApp:
    def __init__(self, root: tk.Tk) -> None:
        self.root = root
        self.root.title("ScanPDF Converter")
        self.root.geometry("760x520")

        self.input_var = tk.StringVar()
        self.output_var = tk.StringVar(value=str(ROOT / "output" / "generated" / "output.xlsx"))
        self.pages_var = tk.StringVar(value="3")
        self.status_var = tk.StringVar(value="Sẵn sàng")

        self._build_ui()

    def _build_ui(self) -> None:
        frame = ttk.Frame(self.root, padding=16)
        frame.pack(fill="both", expand=True)

        ttk.Label(frame, text="PDF đầu vào").grid(row=0, column=0, sticky="w")
        ttk.Entry(frame, textvariable=self.input_var, width=70).grid(row=1, column=0, sticky="ew", padx=(0, 8))
        ttk.Button(frame, text="Chọn file", command=self.pick_input).grid(row=1, column=1, sticky="ew")

        ttk.Label(frame, text="Excel đầu ra").grid(row=2, column=0, sticky="w", pady=(12, 0))
        ttk.Entry(frame, textvariable=self.output_var, width=70).grid(row=3, column=0, sticky="ew", padx=(0, 8))
        ttk.Button(frame, text="Lưu thành", command=self.pick_output).grid(row=3, column=1, sticky="ew")

        options = ttk.Frame(frame)
        options.grid(row=4, column=0, columnspan=2, sticky="ew", pady=(12, 0))
        ttk.Label(options, text="Số trang chạy thử").pack(side="left")
        ttk.Entry(options, textvariable=self.pages_var, width=8).pack(side="left", padx=(8, 0))
        ttk.Button(options, text="Chạy", command=self.run_process).pack(side="right")

        ttk.Label(frame, textvariable=self.status_var).grid(row=5, column=0, columnspan=2, sticky="w", pady=(12, 4))

        self.log = tk.Text(frame, wrap="word", height=20)
        self.log.grid(row=6, column=0, columnspan=2, sticky="nsew")

        scroll = ttk.Scrollbar(frame, orient="vertical", command=self.log.yview)
        scroll.grid(row=6, column=2, sticky="ns")
        self.log.configure(yscrollcommand=scroll.set)

        frame.columnconfigure(0, weight=1)
        frame.rowconfigure(6, weight=1)

    def pick_input(self) -> None:
        path = filedialog.askopenfilename(filetypes=[("PDF files", "*.pdf")])
        if path:
            self.input_var.set(path)
            default_output = ROOT / "output" / "generated" / (Path(path).stem + ".xlsx")
            self.output_var.set(str(default_output))

    def pick_output(self) -> None:
        path = filedialog.asksaveasfilename(defaultextension=".xlsx", filetypes=[("Excel files", "*.xlsx")])
        if path:
            self.output_var.set(path)

    def append_log(self, text: str) -> None:
        self.log.insert("end", text + "\n")
        self.log.see("end")

    def run_process(self) -> None:
        input_pdf = self.input_var.get().strip()
        output_xlsx = self.output_var.get().strip()
        if not input_pdf:
            messagebox.showerror("Thiếu file", "Chọn file PDF trước đã.")
            return

        try:
            limit_pages = int(self.pages_var.get().strip()) if self.pages_var.get().strip() else None
        except ValueError:
            messagebox.showerror("Sai dữ liệu", "Số trang phải là số nguyên.")
            return

        self.status_var.set("Đang xử lý...")
        self.append_log(f"[START] {input_pdf}")

        def worker() -> None:
            try:
                result = process_pdf(
                    pdf_path=input_pdf,
                    work_root=ROOT / "output" / "artifacts",
                    output_xlsx=output_xlsx,
                    limit_pages=limit_pages,
                )
                self.root.after(0, lambda: self._on_success(result.template_id, len(result.pages), len(result.parsed_rows), output_xlsx, result.warnings))
            except Exception as exc:
                self.root.after(0, lambda: self._on_error(exc))

        threading.Thread(target=worker, daemon=True).start()

    def _on_success(self, template_id: str | None, pages: int, rows: int, output_xlsx: str, warnings: list[str]) -> None:
        self.status_var.set("Xử lý xong")
        self.append_log(f"[DONE] template={template_id or 'unknown'} pages={pages} rows={rows}")
        for warning in warnings:
            self.append_log(f"[WARN] {warning}")
        self.append_log(f"[OUT] {output_xlsx}")
        messagebox.showinfo("Xong", f"Đã xuất file:\n{output_xlsx}")

    def _on_error(self, exc: Exception) -> None:
        self.status_var.set("Lỗi")
        self.append_log(f"[ERROR] {exc}")
        messagebox.showerror("Lỗi", str(exc))


def main() -> None:
    root = tk.Tk()
    try:
        ttk.Style().theme_use("clam")
    except Exception:
        pass
    app = ScanPdfApp(root)
    app.append_log("ScanPDF GUI ready.")
    root.mainloop()


if __name__ == "__main__":
    main()
