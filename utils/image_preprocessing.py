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

    # 2. Upscale image (IMPORTANT for small text/ads)
    # We use 2x scale with cubic interpolation
    upscaled = cv2.resize(gray, None, fx=2, fy=2, interpolation=cv2.INTER_CUBIC)

    # 3. Noise removal using Bilateral Filter
    # Bilateral filter is excellent for OCR because it smooths noise but preserves sharp edges
    denoised = cv2.bilateralFilter(upscaled, 9, 75, 75)

    # 4. Apply Otsu's thresholding
    # This is often more stable for poster-style images than adaptive thresholding
    _, thresh = cv2.threshold(denoised, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)

    # 5. Optional: Dilation to thicken text (helps with thin/stylized fonts)
    kernel = np.ones((2, 2), np.uint8)
    processed = cv2.dilate(thresh, kernel, iterations=1)

    # Convert back to PIL Image so it can be handled easily by pytesseract
    processed_image = Image.fromarray(processed)
    
    return processed_image
