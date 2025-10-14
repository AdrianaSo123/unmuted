#!/usr/bin/env python3
"""
AI Image Generator for Unmuted Show Cards
Generates high-quality show images using Google Gemini or OpenAI DALL-E
"""

import os
import sys
import requests
import time
import json
from pathlib import Path
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

class ShowImageGenerator:
    def __init__(self):
        self.ai_model = os.getenv('AI_MODEL', 'gemini').lower()
        self.size = os.getenv('IMAGE_SIZE', '1024x1024')
        self.quality = os.getenv('IMAGE_QUALITY', 'standard')
        
        # Set up API based on model choice
        if self.ai_model == 'gemini':
            self.api_key = os.getenv('GOOGLE_AI_API_KEY')
            if not self.api_key:
                raise ValueError("GOOGLE_AI_API_KEY not found in .env file")
            # Note: Google's Imagen API is currently limited access
            # For now, we'll fall back to a simpler approach
            print("⚠️  Note: Google's Imagen API requires special access.")
            print("🔄 Switching to programmatic image generation...")
            self.ai_model = 'programmatic'
        else:
            # Default to OpenAI
            self.api_key = os.getenv('OPENAI_API_KEY')
            if not self.api_key:
                raise ValueError("OPENAI_API_KEY not found in .env file")
            import openai
            openai.api_key = self.api_key
        
        # Define output directories
        self.static_dir = Path("static/images/shows")
        self.docs_dir = Path("docs/images/shows")
        
        # Create directories if they don't exist
        self.static_dir.mkdir(parents=True, exist_ok=True)
        self.docs_dir.mkdir(parents=True, exist_ok=True)

    def get_show_prompts(self):
        """Define prompts for each show with critical analysis focus"""
        return {
            "gossipgirl": {
                "filename": "gossipgirl.jpg",
                "prompt": """Create a sophisticated collage representing Gossip Girl's themes of wealth, privilege, and social dynamics. Include elements like: Manhattan Upper East Side skyline, luxury fashion items, champagne glasses, designer shopping bags, and subtle symbols of class divide. Style should be glamorous but with undertones suggesting the problematic nature of extreme wealth. Color palette: rich golds, deep blues, and elegant blacks. Modern, cinematic composition that captures both the allure and critique of elite society."""
            },
            "pll": {
                "filename": "pll.jpg", 
                "prompt": """Design a mysterious and dramatic composition for Pretty Little Liars focusing on themes of secrets, friendship, and questionable relationships. Include elements like: shadowy figures, vintage keys, old letters or diary pages, masks, and subtle warning symbols. The mood should suggest both teen friendship and underlying danger. Color palette: deep purples, mysterious blacks, and warning reds. Cinematic style that captures the show's blend of teen drama and psychological thriller elements."""
            },
            "teenwolf": {
                "filename": "teenwolf.jpg",
                "prompt": """Create a dynamic supernatural composition for Teen Wolf emphasizing themes of identity, transformation, and LGBTQ+ representation. Include elements like: full moon, forest silhouettes, diverse group of friends, symbols of acceptance and belonging, and subtle rainbow elements. The style should be both mystical and inclusive. Color palette: deep forest greens, moonlight silvers, and pride flag colors subtly integrated. Modern fantasy aesthetic that celebrates diversity and supernatural coming-of-age."""
            },
            "tvd": {
                "filename": "tvd.jpg",
                "prompt": """Design a dark romantic gothic composition for The Vampire Diaries focusing on toxic relationships and supernatural drama. Include elements like: Victorian mansion, dark roses, antique jewelry, blood-red wine glasses, and symbols of eternal but problematic love. Style should be romantically dark but hint at the toxic nature of immortal relationships. Color palette: deep crimsons, gothic blacks, and antique golds. Gothic romance aesthetic with underlying critique of romanticized toxicity."""
            },
            "glee": {
                "filename": "glee.jpg",
                "prompt": """Create a vibrant musical composition for Glee representing both celebration and critique of diversity representation. Include elements like: colorful music notes, diverse hands reaching together, microphones, stage lights, and symbols of both inclusion and performative diversity. Style should be energetic but thoughtful. Color palette: bright rainbow colors with some muted tones to suggest complexity. Musical theater aesthetic that captures both joy and the problems with surface-level representation."""
            },
            "oc": {
                "filename": "oc.jpg",
                "prompt": """Design a sun-soaked California composition for The O.C. focusing on class differences and cultural clash themes. Include elements like: Orange County beaches, luxury homes vs. modest neighborhoods, surfboards, palm trees, and symbols of economic disparity. Style should be bright and beachy but with undertones of social commentary. Color palette: sunny oranges, ocean blues, and golden California light. West Coast aesthetic that highlights both privilege and authenticity."""
            }
        }

    def generate_image_gemini(self, prompt, filename):
        """Generate image using Google Gemini"""
        try:
            print(f"🎨 Generating image for {filename} using Gemini...")
            
            headers = {
                'Content-Type': 'application/json',
            }
            
            data = {
                "prompt": {
                    "text": prompt
                },
                "generationConfig": {
                    "aspectRatio": "1:1",
                    "outputMimeType": "image/jpeg"
                }
            }
            
            url = f"{self.base_url}?key={self.api_key}"
            response = requests.post(url, headers=headers, json=data)
            response.raise_for_status()
            
            result = response.json()
            
            # Gemini returns base64 encoded image
            import base64
            if 'generatedImages' in result and len(result['generatedImages']) > 0:
                image_data = base64.b64decode(result['generatedImages'][0]['bytesBase64Encoded'])
                
                # Save to both directories
                static_path = self.static_dir / filename
                docs_path = self.docs_dir / filename
                
                with open(static_path, 'wb') as f:
                    f.write(image_data)
                
                with open(docs_path, 'wb') as f:
                    f.write(image_data)
                
                print(f"✅ Successfully generated {filename}")
                return True
            else:
                print(f"❌ No image data returned for {filename}")
                return False
                
        except Exception as e:
            print(f"❌ Error generating {filename}: {str(e)}")
            return False

    def generate_image_openai(self, prompt, filename):
        """Generate image using OpenAI DALL-E"""
        try:
            print(f"🎨 Generating image for {filename} using DALL-E...")
            
            import openai
            response = openai.Image.create(
                model="dall-e-3",
                prompt=prompt,
                size=self.size,
                quality=self.quality,
                n=1
            )
            
            # Get the image URL
            image_url = response.data[0].url
            
            # Download the image
            image_response = requests.get(image_url)
            image_response.raise_for_status()
            
            # Save to both static and docs directories
            static_path = self.static_dir / filename
            docs_path = self.docs_dir / filename
            
            with open(static_path, 'wb') as f:
                f.write(image_response.content)
            
            with open(docs_path, 'wb') as f:
                f.write(image_response.content)
            
            print(f"✅ Successfully generated {filename}")
            return True
            
        except Exception as e:
            print(f"❌ Error generating {filename}: {str(e)}")
            return False

    def create_show_specific_image(self, show_id):
        """Create show-specific images with recognizable elements"""
        from PIL import Image, ImageDraw, ImageFont
        
        # Create base image
        img = Image.new('RGB', (1024, 1024), (20, 20, 20))
        draw = ImageDraw.Draw(img)
        
        if show_id == 'gossipgirl':
            # NYC skyline silhouette with luxury elements
            # Background: Manhattan colors
            for y in range(1024):
                ratio = y / 1024
                r = int(25 * (1 - ratio) + 72 * ratio)
                g = int(25 * (1 - ratio) + 61 * ratio) 
                b = int(112 * (1 - ratio) + 139 * ratio)
                draw.line([(0, y), (1024, y)], fill=(r, g, b))
            
            # Draw stylized NYC skyline
            buildings = [
                (50, 600, 150, 1024),   # Building 1
                (150, 500, 250, 1024),  # Building 2 (taller)
                (250, 650, 350, 1024),  # Building 3
                (350, 400, 450, 1024),  # Building 4 (tallest)
                (450, 550, 550, 1024),  # Building 5
                (550, 700, 650, 1024),  # Building 6
                (650, 480, 750, 1024),  # Building 7
                (750, 600, 850, 1024),  # Building 8
                (850, 520, 950, 1024),  # Building 9
            ]
            
            for building in buildings:
                draw.rectangle(building, fill=(10, 10, 10, 180))
                # Add windows
                for window_y in range(building[1] + 20, building[3] - 20, 40):
                    for window_x in range(building[0] + 15, building[2] - 15, 25):
                        if (window_x + window_y) % 3 == 0:  # Random window pattern
                            draw.rectangle([window_x, window_y, window_x + 8, window_y + 15], 
                                         fill=(255, 215, 0))  # Golden windows
            
        elif show_id == 'pll':
            # Dark mysterious house with "A" elements
            # Background: Purple mystery
            for y in range(1024):
                ratio = y / 1024
                r = int(75 * (1 - ratio) + 138 * ratio)
                g = int(0 * (1 - ratio) + 43 * ratio)
                b = int(130 * (1 - ratio) + 226 * ratio)
                draw.line([(0, y), (1024, y)], fill=(r, g, b))
            
            # Draw mysterious house silhouette
            house_points = [
                (300, 400), (500, 300), (700, 400),  # Roof
                (700, 700), (300, 700)  # Walls
            ]
            draw.polygon(house_points, fill=(20, 20, 20))
            
            # Add windows with mysterious glow
            windows = [(350, 450), (450, 450), (550, 450), (650, 450),
                      (350, 550), (450, 550), (550, 550), (650, 550)]
            for wx, wy in windows:
                draw.rectangle([wx, wy, wx + 40, wy + 60], fill=(220, 20, 60))
            
            # Add large "A" symbol
            try:
                a_font = ImageFont.truetype("/System/Library/Fonts/Helvetica.ttc", 200)
                draw.text((450, 150), "A", font=a_font, fill=(255, 255, 255), anchor="mm")
            except:
                draw.text((450, 150), "A", fill=(255, 255, 255), anchor="mm")
                
        elif show_id == 'teenwolf':
            # Forest with full moon and pack elements
            # Background: Forest green
            for y in range(1024):
                ratio = y / 1024
                r = int(34 * (1 - ratio) + 0 * ratio)
                g = int(139 * (1 - ratio) + 100 * ratio)
                b = int(34 * (1 - ratio) + 0 * ratio)
                draw.line([(0, y), (1024, y)], fill=(r, g, b))
            
            # Draw full moon
            draw.ellipse([350, 50, 650, 350], fill=(255, 255, 200))
            
            # Draw forest silhouette
            trees = [
                (50, 600, 150, 1024),
                (120, 550, 200, 1024),
                (180, 580, 260, 1024),
                (240, 520, 320, 1024),
                (700, 540, 780, 1024),
                (760, 580, 840, 1024),
                (820, 550, 900, 1024),
                (880, 600, 960, 1024)
            ]
            
            for tree in trees:
                # Tree trunk
                draw.rectangle(tree, fill=(20, 20, 20))
                # Tree top (triangle)
                top_y = tree[1] - 100
                draw.polygon([
                    (tree[0] + (tree[2] - tree[0])//2, top_y),
                    (tree[0] - 30, tree[1]),
                    (tree[2] + 30, tree[1])
                ], fill=(20, 40, 20))
                
        elif show_id == 'tvd':
            # Gothic mansion with vampire elements
            # Background: Deep red to black
            for y in range(1024):
                ratio = y / 1024
                r = int(139 * (1 - ratio) + 75 * ratio)
                g = int(0 * (1 - ratio) + 0 * ratio)
                b = int(0 * (1 - ratio) + 130 * ratio)
                draw.line([(0, y), (1024, y)], fill=(r, g, b))
            
            # Draw gothic mansion
            # Main structure
            draw.rectangle([200, 400, 800, 800], fill=(30, 30, 30))
            # Towers
            draw.rectangle([150, 300, 250, 800], fill=(25, 25, 25))
            draw.rectangle([750, 300, 850, 800], fill=(25, 25, 25))
            # Roof
            draw.polygon([(200, 400), (500, 250), (800, 400)], fill=(20, 20, 20))
            
            # Add gothic windows
            windows = [(230, 450), (330, 450), (430, 450), (530, 450), (630, 450), (730, 450)]
            for wx, wy in windows:
                draw.rectangle([wx, wy, wx + 30, wy + 80], fill=(139, 0, 0))
                # Gothic arch top
                draw.arc([wx, wy, wx + 30, wy + 30], 0, 180, fill=(139, 0, 0))
                
        elif show_id == 'glee':
            # Stage with spotlights and musical elements
            # Background: Bright stage colors
            for y in range(1024):
                ratio = y / 1024
                r = int(255 * (1 - ratio) + 255 * ratio)
                g = int(20 * (1 - ratio) + 69 * ratio)
                b = int(147 * (1 - ratio) + 0 * ratio)
                draw.line([(0, y), (1024, y)], fill=(r, g, b))
            
            # Draw stage
            draw.rectangle([100, 600, 900, 800], fill=(139, 69, 19))  # Wood stage
            
            # Add spotlights
            spotlight_centers = [(200, 200), (500, 150), (800, 200)]
            for sx, sy in spotlight_centers:
                # Spotlight beam
                draw.polygon([(sx, sy), (sx - 100, 600), (sx + 100, 600)], 
                           fill=(255, 255, 255, 100))
                # Spotlight fixture
                draw.ellipse([sx - 30, sy - 20, sx + 30, sy + 20], fill=(50, 50, 50))
            
            # Add musical notes
            note_positions = [(300, 400), (500, 350), (700, 380), (400, 450), (600, 420)]
            try:
                note_font = ImageFont.truetype("/System/Library/Fonts/Helvetica.ttc", 60)
                for nx, ny in note_positions:
                    draw.text((nx, ny), "♪", font=note_font, fill=(255, 255, 255))
            except:
                for nx, ny in note_positions:
                    draw.text((nx, ny), "♪", fill=(255, 255, 255))
                    
        elif show_id == 'oc':
            # California beach with palm trees and class divide
            # Background: Orange County sunset
            for y in range(1024):
                ratio = y / 1024
                r = int(255 * (1 - ratio) + 30 * ratio)
                g = int(140 * (1 - ratio) + 144 * ratio)
                b = int(0 * (1 - ratio) + 255 * ratio)
                draw.line([(0, y), (1024, y)], fill=(r, g, b))
            
            # Draw beach
            draw.rectangle([0, 700, 1024, 1024], fill=(238, 203, 173))  # Sand
            
            # Draw ocean
            draw.rectangle([0, 600, 1024, 700], fill=(30, 144, 255))  # Ocean
            
            # Add palm trees
            palm_positions = [(150, 500), (300, 480), (700, 490), (850, 510)]
            for px, py in palm_positions:
                # Palm trunk
                draw.rectangle([px - 10, py, px + 10, py + 200], fill=(139, 69, 19))
                # Palm fronds
                frond_points = [
                    [(px, py), (px - 80, py - 50), (px - 60, py - 30)],
                    [(px, py), (px + 80, py - 50), (px + 60, py - 30)],
                    [(px, py), (px - 30, py - 80), (px - 10, py - 60)],
                    [(px, py), (px + 30, py - 80), (px + 10, py - 60)]
                ]
                for frond in frond_points:
                    draw.polygon(frond, fill=(34, 139, 34))
        
        return img

    def generate_image_programmatic(self, prompt, filename):
        """Generate photo-style images with clean overlays"""
        try:
            print(f"🎨 Creating photo-style image for {filename}...")
            
            from PIL import Image, ImageDraw, ImageFont, ImageFilter, ImageEnhance
            import io
            
            # Get show ID from filename
            show_id = filename.replace('.jpg', '')
            
            # Define clean show info
            show_info = {
                'gossipgirl': {
                    'title': 'GOSSIP GIRL',
                    'subtitle': 'Critical Analysis: Wealth, Class & Power Dynamics'
                },
                'pll': {
                    'title': 'PRETTY LITTLE LIARS', 
                    'subtitle': 'Critical Analysis: Secrets, Friendship & Toxic Relationships'
                },
                'teenwolf': {
                    'title': 'TEEN WOLF',
                    'subtitle': 'Critical Analysis: Identity, LGBTQ+ Rep & Supernatural Metaphors'
                },
                'tvd': {
                    'title': 'THE VAMPIRE DIARIES',
                    'subtitle': 'Critical Analysis: Romance, Consent & Toxic Dynamics'
                },
                'glee': {
                    'title': 'GLEE',
                    'subtitle': 'Critical Analysis: Diversity, Representation & Performative Inclusion'
                },
                'oc': {
                    'title': 'THE O.C.',
                    'subtitle': 'Critical Analysis: Class, Culture & California Dreams'
                }
            }
            
            info = show_info.get(show_id, show_info['gossipgirl'])
            
            # Create show-specific image with recognizable elements
            base_img = self.create_show_specific_image(show_id)
            
            # Ensure image is the right size
            base_img = base_img.resize((1024, 1024), Image.Resampling.LANCZOS)
            
            # Darken the image for better text readability
            enhancer = ImageEnhance.Brightness(base_img)
            base_img = enhancer.enhance(0.4)  # Make it darker
            
            # Add subtle blur for text overlay area
            overlay_area = base_img.copy()
            overlay_area = overlay_area.filter(ImageFilter.GaussianBlur(radius=3))
            
            # Create overlay for text
            overlay = Image.new('RGBA', (1024, 1024), (0, 0, 0, 0))
            overlay_draw = ImageDraw.Draw(overlay)
            
            # Add dark gradient overlay at bottom for text
            for y in range(512, 1024):
                alpha = int(((y - 512) / 512) * 180)  # Gradient from transparent to dark
                overlay_draw.line([(0, y), (1024, y)], fill=(0, 0, 0, alpha))
            
            # Composite the overlay
            img = Image.alpha_composite(base_img.convert('RGBA'), overlay).convert('RGB')
            draw = ImageDraw.Draw(img)
            
            # Add clean typography
            try:
                title_font = ImageFont.truetype("/System/Library/Fonts/Helvetica.ttc", 56)
                subtitle_font = ImageFont.truetype("/System/Library/Fonts/Helvetica.ttc", 24)
            except:
                title_font = ImageFont.load_default()
                subtitle_font = ImageFont.load_default()
            
            # Add title at bottom
            title_bbox = draw.textbbox((0, 0), info['title'], font=title_font)
            title_w = title_bbox[2] - title_bbox[0]
            title_x = (1024 - title_w) // 2
            title_y = 750
            
            # Title with shadow for readability
            draw.text((title_x + 3, title_y + 3), info['title'], font=title_font, fill=(0, 0, 0))
            draw.text((title_x, title_y), info['title'], font=title_font, fill=(255, 255, 255))
            
            # Add subtitle
            # Split subtitle into multiple lines if too long
            subtitle_lines = []
            words = info['subtitle'].split(' ')
            current_line = []
            
            for word in words:
                test_line = ' '.join(current_line + [word])
                test_bbox = draw.textbbox((0, 0), test_line, font=subtitle_font)
                if test_bbox[2] - test_bbox[0] > 900:  # Max width
                    if current_line:
                        subtitle_lines.append(' '.join(current_line))
                        current_line = [word]
                    else:
                        subtitle_lines.append(word)
                else:
                    current_line.append(word)
            
            if current_line:
                subtitle_lines.append(' '.join(current_line))
            
            # Draw subtitle lines
            subtitle_y = 820
            for line in subtitle_lines:
                subtitle_bbox = draw.textbbox((0, 0), line, font=subtitle_font)
                subtitle_w = subtitle_bbox[2] - subtitle_bbox[0]
                subtitle_x = (1024 - subtitle_w) // 2
                
                # Subtitle with shadow
                draw.text((subtitle_x + 2, subtitle_y + 2), line, font=subtitle_font, fill=(0, 0, 0))
                draw.text((subtitle_x, subtitle_y), line, font=subtitle_font, fill=(255, 255, 255))
                subtitle_y += 35
            
            # Save images
            static_path = self.static_dir / filename
            docs_path = self.docs_dir / filename
            
            img.save(static_path, 'JPEG', quality=90)
            img.save(docs_path, 'JPEG', quality=90)
            
            print(f"✅ Successfully created {filename}")
            return True
            
        except Exception as e:
            print(f"❌ Error creating {filename}: {str(e)}")
            return False

    def generate_image(self, prompt, filename):
        """Generate image using the configured AI model"""
        if self.ai_model == 'programmatic':
            return self.generate_image_programmatic(prompt, filename)
        elif self.ai_model == 'gemini':
            return self.generate_image_gemini(prompt, filename)
        else:
            return self.generate_image_openai(prompt, filename)

    def generate_all_images(self):
        """Generate all show images"""
        print("🚀 Starting AI image generation for Unmuted show cards...")
        print(f"📁 Output directories: {self.static_dir} and {self.docs_dir}")
        print(f"🤖 Using model: {self.ai_model}")
        print(f"📐 Image size: {self.size}")
        print("-" * 60)
        
        prompts = self.get_show_prompts()
        success_count = 0
        
        for show_id, config in prompts.items():
            # Add delay between requests to respect rate limits
            if success_count > 0:
                print("⏳ Waiting 10 seconds between requests...")
                time.sleep(10)
            
            success = self.generate_image(config['prompt'], config['filename'])
            if success:
                success_count += 1
        
        print("-" * 60)
        print(f"🎉 Generation complete! {success_count}/{len(prompts)} images generated successfully.")
        
        if success_count == len(prompts):
            print("✅ All images generated successfully!")
            print("🔄 Run 'python3 site.py build' to update your site with the new images.")
        else:
            print("⚠️  Some images failed to generate. Check the errors above.")

def main():
    """Main function"""
    try:
        generator = ShowImageGenerator()
        generator.generate_all_images()
    except ValueError as e:
        print(f"❌ Configuration error: {e}")
        print("💡 Make sure to:")
        print("   1. Copy .env.example to .env")
        print("   2. Add your OpenAI API key to the .env file")
        print("   3. Get an API key from: https://platform.openai.com/api-keys")
        sys.exit(1)
    except Exception as e:
        print(f"❌ Unexpected error: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
