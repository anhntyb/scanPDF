from __future__ import annotations

from pathlib import Path

import cv2


def preprocess_image(input_path: str | Path, output_path: str | Path) -> Path:
    src = str(input_path)
    dst = Path(output_path)
    dst.parent.mkdir(parents=True, exist_ok=True)

    image = cv2.imread(src)
    if image is None:
        raise ValueError(f"Unable to read image: {input_path}")

    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    blur = cv2.GaussianBlur(gray, (3, 3), 0)
    processed = cv2.adaptiveThreshold(
        blur,
        255,
        cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
        cv2.THRESH_BINARY,
        35,
        15,
    )

    cv2.imwrite(str(dst), processed)
    return dst
