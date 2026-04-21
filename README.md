# Image to Text Generator

A complete AI-powered Python web application built with Flask for extracting text from images (OCR) and generating human-readable image captions.

## Main Purpose
The core functionality of this application is **Image to Text Extraction (OCR)**. It uses Tesseract OCR as the primary engine for fast and reliable extraction.

- **OCR System**: Extracts text using Tesseract.
- **Image Preprocessing**: Auto-converts to grayscale, applies thresholding, and reduces noise to optimize OCR results.
- **Web UI**: Modern, clean, TailwindCSS-powered frontend with drag-and-drop support.
- **Developer API**: Built-in REST endpoint `/api/process-image`.

## Prerequisites
- Python 3.10+
- **Tesseract OCR Engine**: You must install Tesseract OCR on your system.
  - **Windows**: Download the installer from [UB-Mannheim/tesseract](https://github.com/UB-Mannheim/tesseract/wiki). Ensure you add Tesseract to your System PATH during installation.

## Installation

1. Clone or navigate to the project directory:
   ```bash
   cd image-to-text-generator
   ```

2. Install Python dependencies:
   ```bash
   pip install -r requirements.txt
   ```
venv\Scripts\activate
## Running the Application

1. Start the Flask server:
   ```bash
   python app.py
   ```

2. Open your web browser and navigate to:
   ```
   http://127.0.0.1:5000
   ```
"# image-to-text-generator" 
"# image-to-text-generator" 
