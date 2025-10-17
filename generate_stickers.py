#!/usr/bin/env python3
"""
Generate sticker designs for Unmuted merch using DALL-E 3
"""

import os
from pathlib import Path
import time
import requests

# Get API key
api_key = os.getenv('OPENAI_API_KEY')
if api_key:
    api_key = api_key.strip()

# Output directory
output_dir = Path('static/images/shop/stickers')
output_dir.mkdir(parents=True, exist_ok=True)

# Sticker designs with prompts - Clean sticker aesthetic
stickers = [
    {
        "name": "unmuted-wordmark-sticker",
        "prompt": "A die-cut vinyl sticker mockup. The word 'UNMUTED' in bold sans-serif font. Purple (#9333EA) text with a thin white outline/border around each letter. Shown on a white surface with subtle shadow underneath to show it's a sticker. Clean, professional product photo style."
    },
    {
        "name": "representation-matters-sticker",
        "prompt": "A rectangular vinyl sticker mockup with rounded corners. Text reads 'REPRESENTATION MATTERS' in bold uppercase font. Purple (#9333EA) background with white text. Thin white border around the edge. Shown on a white surface with subtle shadow. Product photography style."
    },
    {
        "name": "critical-analysis-sticker",
        "prompt": "A die-cut vinyl sticker mockup. Text reads 'CRITICAL ANALYSIS' in bold uppercase sans-serif font. Pink (#EC4899) text with thin white outline. Shown on a white surface with subtle shadow underneath. Clean product photo style."
    },
    {
        "name": "diverse-voices-sticker",
        "prompt": "A rounded rectangle vinyl sticker mockup. Text reads 'DIVERSE VOICES' in bold uppercase font. Coral (#FF6B6B) background with white text. White border around edge. Shown on white surface with shadow. Product photography style."
    },
    {
        "name": "media-literacy-sticker",
        "prompt": "A die-cut vinyl sticker mockup. Text reads 'MEDIA LITERACY' in bold uppercase sans-serif font. Purple (#9333EA) text with thin white outline around letters. Shown on white surface with subtle shadow. Product photo style."
    },
    {
        "name": "unmuted-logo-sticker",
        "prompt": "A circular vinyl sticker mockup. Simple megaphone icon in purple (#9333EA) with 'UNMUTED' text below in bold font. White background, thin purple border around the circle edge. Shown on white surface with shadow. Clean product photography style."
    }
]

def generate_sticker(sticker_info):
    """Generate a single sticker using DALL-E 3"""
    name = sticker_info['name']
    prompt = sticker_info['prompt']
    
    print(f"\n🎨 Generating: {name}")
    print(f"Prompt: {prompt[:100]}...")
    
    try:
        headers = {
            'Authorization': f'Bearer {api_key}',
            'Content-Type': 'application/json'
        }
        
        data = {
            'model': 'dall-e-3',
            'prompt': prompt,
            'n': 1,
            'size': '1024x1024',
            'quality': 'standard'
        }
        
        response = requests.post(
            'https://api.openai.com/v1/images/generations',
            headers=headers,
            json=data
        )
        
        if response.status_code != 200:
            print(f"API Error {response.status_code}: {response.text}")
        
        response.raise_for_status()
        
        result = response.json()
        image_url = result['data'][0]['url']
        
        # Download the image
        image_response = requests.get(image_url)
        image_response.raise_for_status()
        
        output_path = output_dir / f"{name}.png"
        
        with open(output_path, 'wb') as f:
            f.write(image_response.content)
        
        print(f"✅ Generated! Saved to: {output_path}")
        return True
        
    except Exception as e:
        print(f"❌ Error generating {name}: {e}")
        return False

def main():
    print("=" * 60)
    print("🎨 UNMUTED STICKER GENERATOR")
    print("=" * 60)
    print(f"\nGenerating {len(stickers)} sticker designs...")
    print(f"Output directory: {output_dir.absolute()}\n")
    
    # Check for API key
    if not api_key:
        print("❌ Error: OPENAI_API_KEY not found in environment variables")
        print("Please set it in your .env file or export it:")
        print("export OPENAI_API_KEY='your-key-here'")
        return
    
    success_count = 0
    
    for i, sticker in enumerate(stickers, 1):
        print(f"\n[{i}/{len(stickers)}]", end=" ")
        if generate_sticker(sticker):
            success_count += 1
        
        # Rate limiting - wait between requests
        if i < len(stickers):
            print("⏳ Waiting 5 seconds before next generation...")
            time.sleep(5)
    
    print("\n" + "=" * 60)
    print(f"✅ Complete! Generated {success_count}/{len(stickers)} stickers")
    print(f"📁 Check: {output_dir.absolute()}")

if __name__ == "__main__":
    main()
