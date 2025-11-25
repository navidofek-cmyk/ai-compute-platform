#!/usr/bin/env python3
"""Simple single digit test"""

import requests
import json
from PIL import Image, ImageDraw, ImageFont

def create_digit_image(digit):
    """Create 28x28 image with a digit"""
    img = Image.new('L', (28, 28), color=255)  # White background
    draw = ImageDraw.Draw(img)
    
    try:
        font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 20)
    except:
        font = ImageFont.load_default()
    
    text = str(digit)
    bbox = draw.textbbox((0, 0), text, font=font)
    text_width = bbox[2] - bbox[0]
    text_height = bbox[3] - bbox[1]
    
    x = (28 - text_width) // 2
    y = (28 - text_height) // 2 - 2
    
    draw.text((x, y), text, fill=0, font=font)  # Black text
    return img

def image_to_array(img):
    """Convert PIL image to normalized array"""
    import numpy as np
    arr = np.array(img, dtype=np.float32)
    # MNIST convention: black background (0), white digit (1)
    # So invert: 1.0 - (pixel_value / 255.0)
    normalized = 1.0 - (arr / 255.0)
    return normalized.flatten().tolist()

# Test digit 0
print("Creating digit 0...")
img = create_digit_image(0)
img_data = image_to_array(img)

print(f"Data size: {len(img_data)}")
print(f"Data min: {min(img_data):.3f}, max: {max(img_data):.3f}")

payload = {
    "model_name": "mnist",
    "input_data": img_data,
    "input_shape": [1, 1, 28, 28],
    "apply_softmax": True,
    "top_k": 5
}

print("\nSending request to API...")
print(f"Payload size: {len(json.dumps(payload))} bytes")

try:
    response = requests.post(
        "http://localhost:8000/api/v1/ml/inference",
        json=payload,
        timeout=10
    )
    
    print(f"\nStatus: {response.status_code}")
    
    if response.status_code == 200:
        result = response.json()
        print("✅ SUCCESS!")
        print(f"  Inference time: {result['inference_time_ms']:.2f}ms")
        print(f"  Top classes: {result['top_classes']}")
        print(f"  Top probabilities: {result['top_probabilities']}")
    else:
        print(f"❌ ERROR: {response.text}")
        
except Exception as e:
    print(f"❌ EXCEPTION: {type(e).__name__}: {e}")
