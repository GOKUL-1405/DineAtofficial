#!/usr/bin/env python
"""
Test script to verify Gemini API integration
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
    print("❌ GEMINI_API_KEY not found in environment variables")
    print("Please add this to your .env file:")
    print("GEMINI_API_KEY=AIzaSyAFeKBgVblp0KDlbAiTSs2AOuEOvvaH0IM")
    sys.exit(1)

print(f"✅ API key found: {api_key[:20]}...")

# Test Gemini connection
try:
    genai.configure(api_key=api_key)
    model = genai.GenerativeModel('gemini-1.5-flash')
    print("✅ Gemini model initialized successfully")
    
    # Test a simple query
    response = model.generate_content("Hello! Can you respond with 'API test successful'?")
    print(f"✅ API test response: {response.text}")
    
    # Test with project context
    project_info = "DineAt is a restaurant management system with ordering, kitchen dashboard, and admin panel."
    test_prompt = f"""You are a chatbot for a specific software project.

Project details:
{project_info}

Rules:
- Answer only from project details
- Do not use external knowledge
- If unrelated question, say it is outside project scope

User question: What is DineAt?

Provide a helpful response based only on the project information above."""
    
    response = model.generate_content(test_prompt)
    print(f"✅ Project context test response: {response.text}")
    
    print("\n🎉 All tests passed! Your Gemini API integration is working correctly.")
    print("The chatbot should now work on your DineAt website.")
    
except Exception as e:
    print(f"❌ Error testing Gemini API: {e}")
    print("Please check your API key and internet connection.")
    sys.exit(1)
