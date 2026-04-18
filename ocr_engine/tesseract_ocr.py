import pytesseract
from PIL import Image

def extract_text_tesseract(image):
    """
    Extract text using Tesseract OCR.
    Accepts a PIL Image object (typically preprocessed).
    """
    try:
        # Assuming tesseract is in PATH. If not, user needs to uncomment and set the path below:
        # pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'
        
        # We can add a simple language detection or config if needed, but for now, default config.
        text = pytesseract.image_to_string(image)
        return text.strip()
    except Exception as e:
        print(f"Tesseract OCR Error: {e}")
        return ""
