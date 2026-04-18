import os
from flask import Flask, request, render_template, jsonify, send_file
from werkzeug.utils import secure_filename
import tempfile
import io

# Import project modules
from utils.image_preprocessing import preprocess_for_ocr, load_image_for_easyocr
from ocr_engine.tesseract_ocr import extract_text_tesseract
from ocr_engine.easyocr_engine import extract_text_easyocr
from ai_caption.caption_generator import generate_caption

app = Flask(__name__)

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

@app.route('/process', methods=['POST'])
def process_image_web():
    if 'image' not in request.files:
        return jsonify({'error': 'No file part in the request'}), 400
        
    file = request.files['image']
    if file.filename == '':
        return jsonify({'error': 'No selected file'}), 400
        
    if not allowed_file(file.filename):
        return jsonify({'error': 'File type not allowed'}), 400

    if file:
        filename = secure_filename(file.filename)
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(file_path)

        ocr_engine = request.form.get('engine', 'tesseract')

        try:
            # 1. Image Preprocessing & OCR
            ocr_text = ""
            if ocr_engine == 'easyocr':
                ocr_text = extract_text_easyocr(file_path)
            else:
                # Default to Tesseract
                try:
                    preprocessed_img = preprocess_for_ocr(file_path)
                    ocr_text = extract_text_tesseract(preprocessed_img)
                    
                    # Fallback if tesseract fails entirely (empty result or error)
                    if not ocr_text.strip():
                        ocr_text = extract_text_easyocr(file_path)
                except Exception as e:
                    print(f"Preprocessing/Tesseract error: {e}")
                    ocr_text = extract_text_easyocr(file_path)

            if not ocr_text:
                ocr_text = "No text could be extracted from this image."

            # 2. AI Captioning (Advanced Feature)
            # You can make this optional based on a toggle to speed up response
            generate_caption_flag = request.form.get('generate_caption', 'true').lower() == 'true'
            ai_caption = ""
            if generate_caption_flag:
                ai_caption = generate_caption(file_path)

            return jsonify({
                'ocr_text': ocr_text,
                'ai_caption': ai_caption,
                'status': 'success'
            })

        except Exception as e:
            return jsonify({'error': str(e)}), 500

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
    app.run(debug=True, port=5000)
