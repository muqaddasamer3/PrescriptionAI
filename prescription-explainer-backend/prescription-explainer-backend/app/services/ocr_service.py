"""
OCR service.

Two supported modes (set via OCR_ENGINE in .env):
1. "tesseract" - classic OCR via pytesseract. Fast, free, but struggles
   badly with handwriting.
2. "gemma_vision" - skip classic OCR entirely and let Gemma read the image
   directly via its multimodal endpoint. Recommended for handwritten
   prescriptions since handwriting OCR accuracy with Tesseract is poor.
"""

from app.core.config import settings


class OCRError(Exception):
    pass


def extract_text_tesseract(image_path: str) -> str:
    try:
        import pytesseract
        from PIL import Image
    except ImportError as e:
        raise OCRError(
            "pytesseract/Pillow not installed. Run: pip install pytesseract pillow"
        ) from e

    try:
        image = Image.open(image_path)
        text = pytesseract.image_to_string(image)
        if not text.strip():
            raise OCRError("No text could be extracted from the image.")
        return text.strip()
    except Exception as e:
        raise OCRError(f"OCR extraction failed: {e}") from e


def extract_text(image_path: str) -> str:
    """
    Entry point used by the router. When OCR_ENGINE=gemma_vision, this
    returns an empty string on purpose — the raw image is sent straight to
    Gemma's vision-capable endpoint in gemma_service instead, since chaining
    OCR -> text -> LLM compounds errors on messy handwriting.
    """
    if settings.OCR_ENGINE == "gemma_vision":
        return ""
    return extract_text_tesseract(image_path)