# Gemini API Key Setup Instructions

## Your API Key
```
AIzaSyAFeKBgVblp0KDlbAiTSs2AOuEOvvaH0IM
```

## How to Add the API Key

### Method 1: Update .env file (Recommended)
1. Open your `.env` file in the backend directory
2. Add this line to the file:
   ```
   GEMINI_API_KEY=AIzaSyAFeKBgVblp0KDlbAiTSs2AOuEOvvaH0IM
   ```

### Method 2: Set Environment Variable
Run this command in your terminal:
```bash
export GEMINI_API_KEY=AIzaSyAFeKBgVblp0KDlbAiTSs2AOuEOvvaH0IM
```

### Method 3: Windows Environment Variable
```cmd
set GEMINI_API_KEY=AIzaSyAFeKBgVblp0KDlbAiTSs2AOuEOvvaH0IM
```

## Complete .env File Example
Your `.env` file should look like this:

```
# Django Secret Key (Generate a new one for production)
SECRET_KEY=django-insecure-placeholder-key-change-in-production-12345

# Debug Mode (Set to False in production)
DEBUG=True

# Allowed Hosts (Comma-separated)
ALLOWED_HOSTS=localhost,127.0.0.1

# MySQL Database Configuration
DB_NAME=dineat_db
DB_USER=root
DB_PASSWORD=your_mysql_password_here
DB_HOST=localhost
DB_PORT=3306

# Gemini AI Configuration
GEMINI_API_KEY=AIzaSyAFeKBgVblp0KDlbAiTSs2AOuEOvvaH0IM
```

## Install Required Package
Run this command to install the Gemini library:
```bash
pip install google-generativeai==0.8.3
```

## Restart Django Server
After adding the API key, restart your Django server:
```bash
python manage.py runserver
```

## Test the Chatbot
1. Open your browser and go to any page of your DineAt application
2. Click the chatbot bubble in the bottom-right corner
3. Ask a question about your DineAt project
4. The chatbot should now respond with intelligent answers based on your project information!

## Security Note
- Never commit your API key to version control
- The .env file is already in .gitignore for security
- Keep your API key confidential and share only with trusted team members
