#!/usr/bin/env python3
"""
Script to update the API key in .env file
"""
import os
from pathlib import Path

def update_api_key():
    print("API Key Update Script")
    print("=" * 30)
    
    # Get new API key from user
    new_key = input("Enter your new Google Gemini API key: ").strip()
    
    if not new_key:
        print("Error: API key cannot be empty")
        return
    
    # Path to .env file
    env_path = Path(__file__).parent / '.env'
    
    # Read current .env content
    if env_path.exists():
        with open(env_path, 'r') as f:
            lines = f.readlines()
    else:
        lines = []
    
    # Update or add GEMINI_API_KEY
    key_found = False
    for i, line in enumerate(lines):
        if line.startswith('GEMINI_API_KEY='):
            lines[i] = f'GEMINI_API_KEY={new_key}\n'
            key_found = True
            break
    
    if not key_found:
        lines.append(f'GEMINI_API_KEY={new_key}\n')
    
    # Write back to .env
    with open(env_path, 'w') as f:
        f.writelines(lines)
    
    print(f"✅ API key updated in {env_path}")
    print("🔄 Restart your Django server to apply changes")

if __name__ == "__main__":
    update_api_key()
