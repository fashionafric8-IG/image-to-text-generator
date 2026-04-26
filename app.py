import os
from flask import Flask, request, render_template, jsonify, send_file
from werkzeug.utils import secure_filename
import tempfile
import io

# Import project modules
from utils.image_preprocessing import preprocess_for_ocr
from ocr_engine.tesseract_ocr import extract_text_tesseract
from flask_cors import CORS

app = Flask(__name__)
CORS(app, origins=["https://image.toolsflash.org"])

# Configure Uploads
UPLOAD_FOLDER = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'uploads')
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB max limit

ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'webp', 'bmp'}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/', methods=['GET'])
def index():
    return render_template('index.html')

def extract_text(file_path):
    """
    Unified OCR function that applies preprocessing and uses Tesseract.
    """
    try:
        # Preprocess the image
        preprocessed_img = preprocess_for_ocr(file_path)
        
        # Extract text using Tesseract
        ocr_text = extract_text_tesseract(preprocessed_img)
        
        if not ocr_text.strip():
            return "No text could be extracted from this image."
            
        return ocr_text
    except Exception as e:
        print(f"Extraction error details: {str(e)}")
        # We re-raise or return a specific error that the route can catch
        raise Exception(f"OCR Processing failed: {str(e)}")

@app.route('/process', methods=['POST'])
def process_image_web():
    try:
        if 'image' not in request.files:
            return jsonify({'error': 'No file part in the request', 'status': 'error'}), 400
            
        file = request.files['image']
        if file.filename == '':
            return jsonify({'error': 'No selected file', 'status': 'error'}), 400
            
        if not allowed_file(file.filename):
            return jsonify({'error': 'File type not allowed', 'status': 'error'}), 400

        # Create safe filename and path
        filename = secure_filename(file.filename)
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        
        # Save file (this can fail due to permissions/disk space)
        file.save(file_path)

        # 1. Image Preprocessing & OCR (Tesseract Only)
        ocr_text = extract_text(file_path)

        # Cleanup if you want, but usually keep for a while or use tempfile
        # os.remove(file_path) 

        return jsonify({
            'ocr_text': ocr_text,
            'status': 'success'
        })

    except Exception as e:
        # Crucial for production logs
        print(f"CRITICAL ERROR in /process: {str(e)}")
        import traceback
        traceback.print_exc()
        
        return jsonify({
            'error': str(e),
            'status': 'error'
        }), 500

@app.route('/api/process-image', methods=['POST'])
def api_process_image():
    return process_image_web()

@app.route('/api/download-txt', methods=['POST'])
def download_txt():
    data = request.json
    text_content = data.get('text', '')
    
    # Create in-memory file
    mem = io.BytesIO()
    mem.write(text_content.encode('utf-8'))
    mem.seek(0)
    
    return send_file(
        mem,
        as_attachment=True,
        download_name='ocr_extraction.txt',
        mimetype='text/plain'
    )

if __name__ == '__main__':
    app.run(debug=True, port=5001)
