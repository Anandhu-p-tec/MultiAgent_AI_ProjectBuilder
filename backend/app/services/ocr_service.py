import pytesseract
from PIL import Image
import tempfile

def extract_text_from_image(image_file) -> str:
    """Extract text using Tesseract OCR from an image file."""
    with tempfile.NamedTemporaryFile(delete=False) as tmp:
        tmp.write(image_file.read())
        tmp_path = tmp.name

    try:
        img = Image.open(tmp_path)
        text = pytesseract.image_to_string(img)
        return text.strip()
    except Exception as e:
        raise RuntimeError(f"OCR failed: {e}")
