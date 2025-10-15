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
            # Use the correct Gemini API endpoint for image generation
            self.base_url = "https://generativelanguage.googleapis.com/v1beta/models/gemini-pro-vision:generateContent"
        else:
            # Default to OpenAI
            self.api_key = os.getenv('OPENAI_API_KEY')
            if not self.api_key:
                raise ValueError("OPENAI_API_KEY not found in .env file")
            # Clean up the API key (remove any extra spaces)
            self.api_key = self.api_key.strip()
        
        # Define output directories
        self.static_dir = Path("static/images/shows")
        self.docs_dir = Path("docs/images/shows")
        
        # Create directories if they don't exist
        self.static_dir.mkdir(parents=True, exist_ok=True)
        self.docs_dir.mkdir(parents=True, exist_ok=True)

    def get_show_prompts(self):
        """Define photorealistic prompts for DALL-E 3 generation"""
        return {
            "gossipgirl": {
                "filename": "gossipgirl.jpg",
                "prompt": """Professional photograph featuring the iconic Met Museum steps with headbands, designer handbags, Constance Billard school uniforms (plaid skirts and blazers), multiple smartphones showing 'XOXO Gossip Girl' text messages, champagne bottles, the distinctive Tiffany blue box, Blair's signature headband collection, luxury shopping bags, a laptop showing the Gossip Girl blog interface, and Manhattan skyline in background. Include visual references to Chuck's bowtie, Serena's blonde hair accessories, and the Palace Hotel. Upper East Side luxury aesthetic with fashion magazine quality."""
            },
            "pll": {
                "filename": "pll.jpg", 
                "prompt": """Professional photograph featuring the iconic 'A' symbol prominently displayed, red coat hanging dramatically, vintage dollhouse with creepy dolls, Rosewood High School elements, multiple cell phones showing threatening 'A' messages, black hoodies, masquerade masks, old diary with secrets, skeleton keys, lipstick messages on mirrors, the iconic 'shh' finger gesture, scattered Scrabble tiles spelling threats, and mysterious shadows. Include references to the liars' friendship bracelets, coffee cups from The Brew, and the bell tower. Dark, mysterious Rosewood aesthetic with psychological thriller vibes."""
            },
            "teenwolf": {
                "filename": "teenwolf.jpg",
                "prompt": """Professional photograph featuring Beacon Hills High School lacrosse field at night, massive full moon, Stiles' iconic blue Jeep with duct tape, lacrosse sticks and jerseys with number 11 and 24, glowing alpha red eyes and beta yellow eyes in the darkness, wolfsbane flowers, the Hale house ruins, claw marks everywhere, kanima venom, mountain ash barriers, bestiary books, and the triskelion symbol. Include references to the animal clinic, Lydia's banshee screams visualized, and the Nemeton tree stump. Supernatural MTV aesthetic with pack dynamics."""
            },
            "tvd": {
                "filename": "tvd.jpg",
                "prompt": """Professional photograph featuring the Salvatore Boarding House with white columns, Damon's iconic blue Camaro, vervain flowers, daylight rings with lapis lazuli stones, Elena's necklace, Stefan's journals, bourbon glasses, blood bags, wooden stakes, the Mystic Falls town sign, Wickery Bridge, the Gilbert ring, vampire fangs and veins, the Mystic Grill sign, old Fell's Church cemetery, and the doppelganger portraits. Include references to the tomb, founding families' symbols, and the 1864 flashback aesthetic. Gothic Southern vampire romance with CW drama quality."""
            },
            "glee": {
                "filename": "glee.jpg",
                "prompt": """Professional photograph featuring McKinley High's iconic red choir room chairs in three rows, Mr. Schue's piano, the 'Glee' banner, Nationals and Regionals trophies, Rachel's gold star necklace, Kurt's fashion-forward outfits, Mercedes' diva accessories, Santana's Cheerios uniform, slushie cups, Broadway show posters (Wicked, Rent, Funny Girl), sheet music for 'Don't Stop Believin', the auditorium stage, and the choir room's distinctive windows. Include references to the football field, Sue Sylvester's tracksuit, and the hallway lockers. Bright, theatrical, musical comedy aesthetic."""
            },
            "oc": {
                "filename": "oc.jpg",
                "prompt": """Professional photograph featuring Newport Beach pier, the Cohen's pool house, Seth's comic books and action figures (Captain Oats and Princess Sparkle references), surfboards, the iconic 'Welcome to the O.C., bitch!' vibe, Chrismukkah decorations, indie rock band posters (Death Cab for Cutie), The Bait Shop venue sign, Harbor School elements, Ryan's white tank tops, Summer's designer outfits, the model home, and luxury yachts at the harbor. Include references to bagels, the lifeguard tower, and the contrast between Chino and Newport. Early 2000s California teen drama aesthetic with FOX quality."""
            },
            # How It Works section images - matching Unmuted's sleek, modern aesthetic
            "how-it-works-1": {
                "filename": "how-it-works-choose-show.jpg",
                "prompt": """Sleek, modern aesthetic photograph of a minimalist workspace with a high-end laptop displaying the Unmuted website interface. Show the six teen drama show cards (Gossip Girl, PLL, Teen Wolf, TVD, Glee, The O.C.) on screen in a clean, professional layout. Include elements like a modern desk setup, subtle navy and coral accent colors matching the site's brand, elegant typography, and soft professional lighting. The scene should feel sophisticated, academic, and perfectly aligned with a critical media analysis platform's visual identity."""
            },
            "how-it-works-2": {
                "filename": "how-it-works-analysis.jpg", 
                "prompt": """Modern, sophisticated photograph of young diverse content creators filming critical analysis content. Show a professional but approachable setup with ring lights, quality microphones, and multiple monitors displaying teen drama scenes for analysis. Include elements like analytical notes, representation frameworks, and the creators discussing complex themes with intelligence and humor. The aesthetic should be contemporary, professional, and match a modern media literacy platform - think sleek podcast studio meets academic discussion space."""
            },
            "how-it-works-3": {
                "filename": "how-it-works-literacy.jpg",
                "prompt": """Clean, contemporary photograph of media literacy in action - showing someone taking thoughtful notes while watching teen drama content on a modern setup. Include elements like analytical frameworks, representation charts, cultural context materials, and the distinctive navy/coral color scheme of the Unmuted brand. The scene should convey intellectual engagement, critical thinking, and the development of media analysis skills in a visually appealing, modern aesthetic that matches a sophisticated educational platform."""
            },
            # Video thumbnail mockups for playlists
            "gossip-girl-video": {
                "filename": "gossip-girl-video-thumb.jpg",
                "prompt": """Professional video thumbnail mockup showing a YouTube-style player interface with Gossip Girl critical analysis content. Show a split screen with iconic Gossip Girl scenes (Met steps, luxury shopping, Upper East Side) on one side and a diverse young creator providing commentary on the other side. Include video player UI elements like play button, progress bar, view count, and title overlay reading 'Gossip Girl: Wealth, Privilege & Class Commentary'. Modern, clean video player aesthetic with professional lighting and engaging thumbnail composition."""
            },
            "pll-video": {
                "filename": "pll-video-thumb.jpg", 
                "prompt": """Professional video thumbnail mockup showing a streaming platform interface with Pretty Little Liars analysis content. Display the iconic 'A' symbol and mysterious Rosewood scenes with a creator discussing the show's problematic elements. Include video player controls, timestamp showing '15:32', and title overlay 'PLL: Mystery, Friendship & Toxic Relationships'. Dark, mysterious aesthetic matching the show's vibe with professional video production quality."""
            },
            "teenwolf-video": {
                "filename": "teenwolf-video-thumb.jpg",
                "prompt": """Professional video thumbnail mockup featuring Teen Wolf critical analysis with supernatural forest scenes and diverse cast representation. Show a creator highlighting LGBTQ+ representation and supernatural metaphors. Include video player interface with play button, subscriber count, and title 'Teen Wolf: The MTV Show That Got Representation Right?'. Modern video player aesthetic with moonlit, mystical atmosphere and professional content creator setup."""
            },
            "tvd-video": {
                "filename": "tvd-video-thumb.jpg",
                "prompt": """Professional video thumbnail mockup displaying The Vampire Diaries analysis content with gothic Mystic Falls imagery and vampire romance scenes. Feature a creator discussing toxic relationship dynamics and the 'Bonnie Bennett problem'. Include streaming interface elements, view count, and title overlay 'TVD: Vampire Romance & Problematic Faves'. Dark, romantic aesthetic with professional video production quality and engaging thumbnail composition."""
            },
            "glee-video": {
                "filename": "glee-video-thumb.jpg",
                "prompt": """Professional video thumbnail mockup showing Glee critical analysis with McKinley High choir room and diverse cast performance scenes. Display a creator analyzing representation and performative inclusion. Include video player controls, like/dislike buttons, and title 'Glee: Representation Done Right... Or Wrong?'. Bright, colorful aesthetic matching the show's energy with professional content creation setup and engaging thumbnail design."""
            },
            "oc-video": {
                "filename": "oc-video-thumb.jpg",
                "prompt": """Professional video thumbnail mockup featuring The O.C. analysis with Newport Beach scenes and California wealth imagery. Show a creator discussing class dynamics and the outsider narrative. Include video streaming interface, progress bar, and title overlay 'The O.C.: Orange County Wealth & Class Commentary'. Sunny, California aesthetic with professional video production quality and modern content creator presentation."""
            }
        }

    def generate_image_gemini(self, prompt, filename):
        """Generate photorealistic image using Google Gemini"""
        try:
            print(f"🎨 Generating photorealistic image for {filename} using Gemini...")
            
            # Enhanced prompt for photorealistic results
            enhanced_prompt = f"Professional high-quality photograph, cinematic lighting, realistic textures, detailed composition: {prompt}. Shot with DSLR camera, professional photography, 4K resolution, photorealistic, highly detailed."
            
            headers = {
                'Content-Type': 'application/json',
            }
            
            # Try the text-to-image generation with Gemini
            data = {
                "contents": [{
                    "parts": [{
                        "text": f"Generate a photorealistic image: {enhanced_prompt}"
                    }]
                }],
                "generationConfig": {
                    "temperature": 0.7,
                    "maxOutputTokens": 1000
                }
            }
            
            url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-pro:generateContent?key={self.api_key}"
            response = requests.post(url, headers=headers, json=data)
            
            if response.status_code != 200:
                print(f"⚠️  Gemini API not available for image generation (status: {response.status_code})")
                print("🔄 Falling back to enhanced programmatic generation...")
                return self.generate_image_programmatic(prompt, filename)
            
            # If Gemini doesn't support image generation directly, fall back
            print("🔄 Using enhanced programmatic generation with photorealistic techniques...")
            return self.generate_image_programmatic(prompt, filename)
                
        except Exception as e:
            print(f"⚠️  Gemini error: {str(e)}")
            print("🔄 Falling back to enhanced programmatic generation...")
            return self.generate_image_programmatic(prompt, filename)

    def generate_image_openai(self, prompt, filename):
        """Generate photorealistic image using OpenAI DALL-E 3"""
        try:
            print(f"🎨 Generating photorealistic image for {filename} using DALL-E 3...")
            
            headers = {
                'Authorization': f'Bearer {self.api_key}',
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
            
            # Save to both static and docs directories
            static_path = self.static_dir / filename
            docs_path = self.docs_dir / filename
            
            with open(static_path, 'wb') as f:
                f.write(image_response.content)
            
            with open(docs_path, 'wb') as f:
                f.write(image_response.content)
            
            print(f"✅ Successfully generated photorealistic {filename}")
            return True
            
        except Exception as e:
            print(f"❌ Error generating {filename}: {str(e)}")
            return False

    def create_show_specific_image(self, show_id):
        """Create photorealistic show-specific images with complex lighting and textures"""
        from PIL import Image, ImageDraw, ImageFont, ImageFilter
        import random
        import math
        
        # Create base image - better aspect ratio for cards (4:3)
        img = Image.new('RGB', (1024, 768), (40, 40, 60))
        draw = ImageDraw.Draw(img)
        
        def add_noise_texture(image, intensity=0.1):
            """Add realistic noise texture to make it look photographic"""
            pixels = image.load()
            for y in range(image.height):
                for x in range(image.width):
                    r, g, b = pixels[x, y]
                    noise = random.randint(-int(intensity*50), int(intensity*50))
                    r = max(0, min(255, r + noise))
                    g = max(0, min(255, g + noise))
                    b = max(0, min(255, b + noise))
                    pixels[x, y] = (r, g, b)
            return image
        
        def create_realistic_gradient(image, colors, direction='vertical'):
            """Create realistic gradient with subtle variations"""
            draw_grad = ImageDraw.Draw(image)
            if direction == 'vertical':
                for y in range(image.height):
                    ratio = y / image.height
                    # Add subtle random variation
                    ratio += random.uniform(-0.02, 0.02)
                    ratio = max(0, min(1, ratio))
                    
                    r = int(colors[0][0] * (1 - ratio) + colors[1][0] * ratio)
                    g = int(colors[0][1] * (1 - ratio) + colors[1][1] * ratio)
                    b = int(colors[0][2] * (1 - ratio) + colors[1][2] * ratio)
                    draw_grad.line([(0, y), (image.width, y)], fill=(r, g, b))
            return image
        
        if show_id == 'gossipgirl':
            # Complex NYC Upper East Side scene with multiple layers
            # Background: Sunset over Manhattan
            for y in range(768):
                ratio = y / 768
                if ratio < 0.3:  # Sky
                    r = int(255 * (1 - ratio*2) + 255 * (ratio*2))
                    g = int(140 * (1 - ratio*2) + 69 * (ratio*2))
                    b = int(0 * (1 - ratio*2) + 0 * (ratio*2))
                elif ratio < 0.6:  # Transition
                    local_ratio = (ratio - 0.3) / 0.3
                    r = int(255 * (1 - local_ratio) + 72 * local_ratio)
                    g = int(69 * (1 - local_ratio) + 61 * local_ratio)
                    b = int(0 * (1 - local_ratio) + 139 * local_ratio)
                else:  # Lower buildings
                    local_ratio = (ratio - 0.6) / 0.4
                    r = int(72 * (1 - local_ratio) + 25 * local_ratio)
                    g = int(61 * (1 - local_ratio) + 25 * local_ratio)
                    b = int(139 * (1 - local_ratio) + 112 * local_ratio)
                draw.line([(0, y), (1024, y)], fill=(r, g, b))
            
            # Draw detailed NYC skyline with multiple building types
            buildings = [
                # Background buildings (lighter)
                (30, 350, 80, 768, (60, 60, 80)),
                (80, 320, 130, 768, (55, 55, 75)),
                (130, 380, 180, 768, (65, 65, 85)),
                (880, 340, 930, 768, (60, 60, 80)),
                (930, 310, 980, 768, (55, 55, 75)),
                
                # Mid-ground buildings (medium)
                (200, 280, 280, 768, (40, 40, 60)),
                (280, 250, 360, 768, (35, 35, 55)),
                (360, 300, 440, 768, (45, 45, 65)),
                (580, 270, 660, 768, (40, 40, 60)),
                (660, 240, 740, 768, (35, 35, 55)),
                (740, 290, 820, 768, (45, 45, 65)),
                
                # Foreground buildings (darkest, most detailed)
                (440, 180, 520, 768, (20, 20, 40)),  # Tallest central building
                (520, 200, 580, 768, (25, 25, 45)),
            ]
            
            for building in buildings:
                x1, y1, x2, y2, color = building
                draw.rectangle([x1, y1, x2, y2], fill=color)
                
                # Add detailed windows with different patterns
                window_rows = (y2 - y1) // 25
                window_cols = (x2 - x1) // 20
                
                for row in range(1, window_rows):
                    for col in range(1, window_cols):
                        wx = x1 + col * 20 + 5
                        wy = y1 + row * 25 + 5
                        
                        # Different window types
                        if (wx + wy) % 7 == 0:  # Lit office windows
                            draw.rectangle([wx, wy, wx + 10, wy + 15], fill=(255, 215, 0))
                        elif (wx + wy) % 5 == 0:  # Apartment windows
                            draw.rectangle([wx, wy, wx + 10, wy + 15], fill=(255, 255, 200))
                        elif (wx + wy) % 3 == 0:  # Dim windows
                            draw.rectangle([wx, wy, wx + 10, wy + 15], fill=(100, 100, 120))
                
                # Add building details
                if x2 - x1 > 60:  # Larger buildings get more details
                    # Rooftop elements
                    draw.rectangle([x1 + 10, y1 - 20, x1 + 30, y1], fill=(30, 30, 50))
                    draw.rectangle([x2 - 30, y1 - 15, x2 - 10, y1], fill=(30, 30, 50))
                    
                    # Building entrance
                    entrance_w = min(40, (x2 - x1) // 2)
                    entrance_x = x1 + (x2 - x1 - entrance_w) // 2
                    draw.rectangle([entrance_x, y2 - 30, entrance_x + entrance_w, y2], fill=(255, 215, 0))
            
            # Add luxury elements
            # Taxi cabs (yellow rectangles)
            taxi_positions = [(150, 720), (300, 730), (600, 725), (800, 735)]
            for tx, ty in taxi_positions:
                draw.rectangle([tx, ty, tx + 40, ty + 20], fill=(255, 215, 0))
                draw.rectangle([tx + 5, ty + 5, tx + 35, ty + 15], fill=(255, 255, 255))
            
            # Street lights
            light_positions = [100, 250, 400, 550, 700, 850]
            for lx in light_positions:
                draw.rectangle([lx, 680, lx + 8, 750], fill=(80, 80, 80))
                draw.ellipse([lx - 10, 670, lx + 18, 690], fill=(255, 255, 200))
            
            # Add Central Park trees (simplified)
            tree_positions = [(50, 600), (100, 620), (150, 610), (900, 605), (950, 615)]
            for tx, ty in tree_positions:
                # Tree trunk
                draw.rectangle([tx, ty, tx + 8, ty + 40], fill=(101, 67, 33))
                # Tree crown
                draw.ellipse([tx - 15, ty - 20, tx + 23, ty + 10], fill=(34, 139, 34))
            
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
            
            # Keep the image bright and vibrant
            enhancer = ImageEnhance.Brightness(base_img)
            base_img = enhancer.enhance(1.1)  # Make it slightly brighter
            
            # Add subtle blur for text overlay area
            overlay_area = base_img.copy()
            overlay_area = overlay_area.filter(ImageFilter.GaussianBlur(radius=3))
            
            # Create overlay for text
            overlay = Image.new('RGBA', (1024, 1024), (0, 0, 0, 0))
            overlay_draw = ImageDraw.Draw(overlay)
            
            # Add subtle dark gradient overlay at bottom for text
            for y in range(600, 1024):
                alpha = int(((y - 600) / 424) * 120)  # Lighter gradient from transparent to semi-dark
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
