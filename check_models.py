#!/usr/bin/env python
"""
Check available Gemini models
"""

import os
import sys
from decouple import config

# Add the project directory to Python path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

try:
    import google.generativeai as genai
    print("✅ google-generativeai package imported successfully")
except ImportError as e:
    print(f"❌ Failed to import google-generativeai: {e}")
    sys.exit(1)

# Test API key
api_key = config('GEMINI_API_KEY', default='')
if not api_key:
    print("❌ GEMINI_API_KEY not found")
    sys.exit(1)

print(f"✅ API key found: {api_key[:20]}...")

# Configure and list models
try:
    genai.configure(api_key=api_key)
    print("✅ Gemini configured successfully")
    
    # List available models
    models = genai.list_models()
    print("\n📋 Available models:")
    for model in models:
        print(f"  - {model.name} (generate_content: {model.supported_generation_methods})")
    
    # Find a suitable model
    suitable_model = None
    for model in models:
        if 'generateContent' in model.supported_generation_methods:
            if 'gemini' in model.name.lower():
                suitable_model = model.name
                break
    
    if suitable_model:
        print(f"\n✅ Found suitable model: {suitable_model}")
        
        # Test the suitable model
        model = genai.GenerativeModel(suitable_model)
        response = model.generate_content("Hello! Please respond with 'API test successful'.")
        print(f"✅ Test response: {response.text}")
        
        # Update the views_chatbot.py file with the correct model name
        views_file = "apps/main/views_chatbot.py"
        if os.path.exists(views_file):
            with open(views_file, 'r') as f:
                content = f.read()
            
            # Replace the model name
            old_model_line = "model = genai.GenerativeModel('gemini-1.5-flash')"
            new_model_line = f"model = genai.GenerativeModel('{suitable_model}')"
            
            if old_model_line in content:
                content = content.replace(old_model_line, new_model_line)
                with open(views_file, 'w') as f:
                    f.write(content)
                print(f"✅ Updated {views_file} with correct model name")
            else:
                print(f"⚠️ Could not find model line to update in {views_file}")
        
    else:
        print("❌ No suitable model found")
    
except Exception as e:
    print(f"❌ Error: {e}")
