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
    # Check if file exists
    import os
    if not os.path.exists(image_path):
        raise FileNotFoundError(f"Image file not found at: {image_path}")

    # Read image using OpenCV
    image = cv2.imread(image_path)
    if image is None:
        raise ValueError(f"OpenCV could not read the image at {image_path}. It might be corrupted or an unsupported format.")

    # 1. Convert to grayscale
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    # 2. Noise removal using median blur
    noise_removed = cv2.medianBlur(gray, 3)

    # 3. Apply thresholding (Otsu's thresholding)
    _, thresh = cv2.threshold(noise_removed, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)

    # Convert back to PIL Image so it can be handled easily by pytesseract
    processed_image = Image.fromarray(thresh)
    
    return processed_image
