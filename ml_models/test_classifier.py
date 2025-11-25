#!/usr/bin/env python3
"""
Generate a test image of a handwritten digit and classify it using the ML API
"""
import requests
import numpy as np
from PIL import Image, ImageDraw, ImageFont
import base64
import io
import json

def create_digit_image(digit, size=(28, 28)):
    """Create a simple handwritten-style digit image"""
    # Create white background
    img = Image.new('L', (280, 280), color=255)
    draw = ImageDraw.Draw(img)
    
    # Try to use a font, fallback to default
    try:
        font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 200)
    except:
        font = ImageFont.load_default()
    
    # Draw the digit in black
    text = str(digit)
    bbox = draw.textbbox((0, 0), text, font=font)
    text_width = bbox[2] - bbox[0]
    text_height = bbox[3] - bbox[1]
    
    position = ((280 - text_width) // 2, (280 - text_height) // 2 - 20)
    draw.text(position, text, fill=0, font=font)
    
    # Resize to 28x28
    img = img.resize(size, Image.LANCZOS)
    
    return img

def image_to_array(img):
    """Convert PIL Image to normalized float array"""
    # Convert to numpy array
    arr = np.array(img, dtype=np.float32)
    
    # Normalize to [0, 1] - MNIST expects white background, black digit
    # So we invert: 0 (black) -> 1.0, 255 (white) -> 0.0
    arr = 1.0 - (arr / 255.0)
    
    return arr.flatten().tolist()

def classify_digit(image_array, api_url="http://localhost:8000"):
    """Send image to ML API for classification"""
    url = f"{api_url}/api/v1/ml/inference"
    
    payload = {
        "model_name": "mnist",
        "input_data": image_array,
        "input_shape": [1, 1, 28, 28],
        "apply_softmax": True,
        "top_k": 3
    }
    
    response = requests.post(url, json=payload)
    response.raise_for_status()
    return response.json()

def main():
    print("=" * 60)
    print("MNIST Digit Classification Demo")
    print("=" * 60)
    
    # Test all digits 0-9
    for digit in range(10):
        print(f"\n🔢 Testing digit: {digit}")
        
        # Create image
        img = create_digit_image(digit)
        
        # Save for inspection
        img.save(f"test_digit_{digit}.png")
        print(f"   Image saved as: test_digit_{digit}.png")
        
        # Convert to array
        img_array = image_to_array(img)
        
        # Classify
        try:
            result = classify_digit(img_array)
            
            print(f"   ✅ Top 3 predictions:")
            if result.get('top_classes') and result.get('top_probabilities'):
                for i, (cls, prob) in enumerate(zip(result['top_classes'], result['top_probabilities'])):
                    print(f"      {i+1}. Digit {cls} - {prob*100:.2f}%")
            
            print(f"   ⏱️  Inference time: {result.get('inference_time_ms', 0):.2f} ms")
            
            # Check if correct
            if result.get('top_classes'):
                top_pred = result['top_classes'][0]
                if top_pred == digit:
                    print(f"   ✅ CORRECT!")
                else:
                    print(f"   ❌ WRONG (predicted {top_pred} instead of {digit})")
                
        except requests.exceptions.ConnectionError:
            print("   ❌ ERROR: Cannot connect to API. Is the gateway running?")
            print("   Run: .\\start_all.ps1")
            return
        except Exception as e:
            print(f"   ❌ ERROR: {e}")
    
    print("\n" + "=" * 60)
    print("Demo complete! Check test_digit_*.png files")
    print("=" * 60)

if __name__ == "__main__":
    main()
