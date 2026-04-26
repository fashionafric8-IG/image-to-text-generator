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

    # 1. Split channels and take the Red channel
    # This provides much better contrast for yellow/orange text on dark backgrounds
    b, g, r = cv2.split(image)
    gray = r

    # 2. Upscale image 3x (Better for complex fonts)
    upscaled = cv2.resize(gray, None, fx=3, fy=3, interpolation=cv2.INTER_CUBIC)

    # 3. Sharpen the image
    # This makes the edges of stylized fonts more distinct for Tesseract
    kernel = np.array([[-1,-1,-1], [-1,9,-1], [-1,-1,-1]])
    sharpened = cv2.filter2D(upscaled, -1, kernel)

    # 4. Noise removal using Bilateral Filter
    denoised = cv2.bilateralFilter(sharpened, 9, 75, 75)

    # 5. Apply Otsu's thresholding
    _, thresh = cv2.threshold(denoised, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)

    # Convert back to PIL Image
    processed_image = Image.fromarray(thresh)
    
    return processed_image
