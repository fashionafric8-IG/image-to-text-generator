import pytesseract
from PIL import Image
import os
import sys

# Auto-configure tesseract path for Windows if not in PATH
if sys.platform.startswith('win'):
    common_paths = [
        r'C:\Program Files\Tesseract-OCR\tesseract.exe',
        r'C:\Program Files (x86)\Tesseract-OCR\tesseract.exe'
    ]
    for p in common_paths:
        if os.path.exists(p):
            pytesseract.pytesseract.tesseract_cmd = p
            break

def extract_text_tesseract(image):
    """
    Extract text using Tesseract OCR.
    Accepts a PIL Image object (typically preprocessed).
    """
    try:
        if not isinstance(image, Image.Image):
            raise TypeError(f"Expected PIL Image object, got {type(image)}")
            
        # We can add a simple language detection or config if needed, but for now, default config.
        text = pytesseract.image_to_string(image)
        return text.strip()
    except Exception as e:
        print(f"Tesseract OCR Error: {e}")
        return ""
