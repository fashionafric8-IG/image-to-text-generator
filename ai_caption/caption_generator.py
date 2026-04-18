from transformers import VisionEncoderDecoderModel, ViTImageProcessor, AutoTokenizer
import torch
from PIL import Image

# Use model 'nlpconnect/vit-gpt2-image-captioning'
MODEL_NAME = "nlpconnect/vit-gpt2-image-captioning"

# Load models globally
try:
    device = "cuda" if torch.cuda.is_available() else "cpu"
    processor = ViTImageProcessor.from_pretrained(MODEL_NAME)
    model = VisionEncoderDecoderModel.from_pretrained(MODEL_NAME).to(device)
    tokenizer = AutoTokenizer.from_pretrained(MODEL_NAME)
    
    max_length = 16
    num_beams = 4
    gen_kwargs = {"max_length": max_length, "num_beams": num_beams}
    
    AI_CAPTIONING_READY = True
except Exception as e:
    print(f"Error loading AI Captioning model: {e}")
    AI_CAPTIONING_READY = False

def generate_caption(image_path):
    """
    Generate an AI caption for the given image.
    """
    if not AI_CAPTIONING_READY:
        return "AI Captioning model failed to load or is not ready."
        
    try:
        image = Image.open(image_path)
        if image.mode != "RGB":
            image = image.convert(mode="RGB")
            
        pixel_values = processor(images=image, return_tensors="pt").pixel_values
        pixel_values = pixel_values.to(device)
        
        output_ids = model.generate(pixel_values, **gen_kwargs)
        
        preds = tokenizer.batch_decode(output_ids, skip_special_tokens=True)
        caption = preds[0].strip()
        
        return caption
    except Exception as e:
        print(f"AI Captioning Error: {e}")
        return "Failed to generate caption."
