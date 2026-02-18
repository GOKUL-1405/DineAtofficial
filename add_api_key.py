#!/usr/bin/env python
"""
Script to add Gemini API key to .env file
"""

import os

# API key to add
api_key_line = "GEMINI_API_KEY=AIzaSyAFeKBgVblp0KDlbAiTSs2AOuEOvvaH0IM"

# Path to .env file
env_file_path = ".env"

# Read existing .env file if it exists
existing_lines = []
if os.path.exists(env_file_path):
    with open(env_file_path, 'r') as f:
        existing_lines = f.readlines()

# Check if GEMINI_API_KEY already exists
key_exists = False
for i, line in enumerate(existing_lines):
    if line.strip().startswith('GEMINI_API_KEY='):
        existing_lines[i] = api_key_line + '\n'
        key_exists = True
        break

# If key doesn't exist, add it
if not key_exists:
    existing_lines.append('\n' + api_key_line + '\n')

# Write back to .env file
with open(env_file_path, 'w') as f:
    f.writelines(existing_lines)

print("✅ Gemini API key added to .env file")
print(f"📝 File: {os.path.abspath(env_file_path)}")
print("\n🔄 Please restart your Django server for changes to take effect:")
print("   python manage.py runserver")
