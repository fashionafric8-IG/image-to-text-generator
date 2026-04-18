import cv2
import numpy as np
from PIL import Image

def preprocess_for_ocr(image_path):
    """
    Preprocess the image to improve OCR accuracy.
    - Convert to grayscale
    - Apply thresholding
    - Noise removal
    """
    # Read image using OpenCV
    image = cv2.imread(image_path)
    if image is None:
        raise ValueError("Could not read the image")

    # 1. Convert to grayscale
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    # 2. Noise removal using median blur
    noise_removed = cv2.medianBlur(gray, 3)

    # 3. Apply thresholding (Otsu's thresholding)
    _, thresh = cv2.threshold(noise_removed, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)

    # Convert back to PIL Image so it can be handled easily by pytesseract
    processed_image = Image.fromarray(thresh)
    
    return processed_image

def load_image_for_easyocr(image_path):
    """
    EasyOCR can read the path directly or use a numpy array.
    We just return the path, or we can use OpenCV image.
    """
    return image_path
