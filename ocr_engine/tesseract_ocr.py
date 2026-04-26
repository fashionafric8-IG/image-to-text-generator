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
            
        # Custom config for better accuracy:
        # --oem 3: Default, based on what is available (LSTM)
        # --psm 1: Automatic page segmentation with OSD. (Most powerful for complex layouts)
        custom_config = r'--oem 3 --psm 1'
        
        text = pytesseract.image_to_string(image, config=custom_config)
        return text.strip()
    except Exception as e:
        print(f"Tesseract OCR Error: {e}")
        return ""
