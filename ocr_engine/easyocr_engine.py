import easyocr

# Initialize reader globally so it doesn't reload on every request
# We only load English by default for speed, can be expanded.
try:
    reader = easyocr.Reader(['en'], gpu=False) # Fallback to CPU to ensure it runs anywhere
except Exception as e:
    print(f"Warning: Failed to initialize EasyOCR: {e}")
    reader = None

def extract_text_easyocr(image_path):
    """
    Extract text using EasyOCR.
    Accepts an image path.
    """
    if reader is None:
        return "EasyOCR is not initialized."
    
    try:
        results = reader.readtext(image_path, detail=0)
        # detail=0 returns just the text string list
        text = "\n".join(results)
        return text.strip()
    except Exception as e:
        print(f"EasyOCR Error: {e}")
        return ""
