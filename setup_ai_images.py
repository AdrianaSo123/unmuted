#!/usr/bin/env python3
"""
Setup script for AI image generation
Helps configure the environment and run image generation
"""

import os
import sys
from pathlib import Path

def setup_environment():
    """Set up the environment for AI image generation"""
    print("🔧 Setting up AI image generation environment...")
    
    # Check if .env file exists
    env_file = Path(".env")
    env_example = Path(".env.example")
    
    if not env_file.exists():
        if env_example.exists():
            print("📋 Copying .env.example to .env...")
            with open(env_example, 'r') as src, open(env_file, 'w') as dst:
                dst.write(src.read())
            print("✅ Created .env file")
        else:
            print("❌ .env.example file not found")
            return False
    
    # Check if API key is set
    from dotenv import load_dotenv
    load_dotenv()
    
    ai_model = os.getenv('AI_MODEL', 'gemini').lower()
    
    if ai_model == 'gemini':
        api_key = os.getenv('GOOGLE_AI_API_KEY')
        if not api_key or api_key == 'your_google_ai_api_key_here':
            print("⚠️  Google AI API key not configured!")
            print("📝 Please edit the .env file and add your Google AI API key:")
            print("   1. Open .env file")
            print("   2. Replace 'your_google_ai_api_key_here' with your actual API key")
            print("   3. Get an API key from: https://aistudio.google.com/app/apikey")
            return False
    else:
        api_key = os.getenv('OPENAI_API_KEY')
        if not api_key or api_key == 'your_openai_api_key_here':
            print("⚠️  OpenAI API key not configured!")
            print("📝 Please edit the .env file and add your OpenAI API key:")
            print("   1. Open .env file")
            print("   2. Replace 'your_openai_api_key_here' with your actual API key")
            print("   3. Get an API key from: https://platform.openai.com/api-keys")
            return False
    
    print("✅ Environment configured successfully!")
    return True

def install_dependencies():
    """Install required dependencies"""
    print("📦 Installing dependencies...")
    os.system("pip install -r requirements.txt")
    print("✅ Dependencies installed!")

def main():
    """Main setup function"""
    print("🎨 Unmuted AI Image Generator Setup")
    print("=" * 50)
    
    # Install dependencies
    install_dependencies()
    
    # Setup environment
    if setup_environment():
        print("\n🚀 Setup complete! You can now run:")
        print("   python3 generate_show_images.py")
        print("\n💡 This will generate AI images for all 6 shows using DALL-E 3")
    else:
        print("\n❌ Setup incomplete. Please configure your API key first.")

if __name__ == "__main__":
    main()
