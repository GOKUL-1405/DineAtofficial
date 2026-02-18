# DineAt Heroku Deployment Guide

## 🚀 Deploy to Heroku

### Prerequisites
- Heroku CLI installed
- Git repository set up
- Heroku account

### Step 1: Install Heroku CLI
```bash
# Download from https://devcenter.heroku.com/articles/heroku-cli
```

### Step 2: Login to Heroku
```bash
heroku login
```

### Step 3: Create Heroku App
```bash
heroku create dineat-restaurant
```

### Step 4: Add PostgreSQL Addon
```bash
heroku addons:create heroku-postgresql:hobby-dev
```

### Step 5: Configure Environment Variables
```bash
heroku config:set SECRET_KEY=$(python -c 'from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())')
heroku config:set DEBUG=False
heroku config:set ALLOWED_HOSTS=dineat-restaurant.herokuapp.com,www.dineat-restaurant.herokuapp.com
heroku config:set GEMINI_API_KEY=your-gemini-api-key
```

### Step 6: Update Settings for Production
Add to `DineAt/settings.py`:
```python
import dj_database_url

# Database
DATABASES = {
    'default': dj_database_url.config(conn_max_age=600)
}

# Static files
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')

# Heroku settings
if 'DYNO' in os.environ:
    SECURE_SSL_REDIRECT = True
    SECURE_HSTS_SECONDS = 31536000
    SECURE_HSTS_INCLUDE_SUBDOMAINS = True
    SECURE_HSTS_PRELOAD = True
```

### Step 7: Add Buildpacks
```bash
heroku buildpacks:add heroku/python
heroku buildpacks:add heroku/nodejs
```

### Step 8: Push to Heroku
```bash
git add .
git commit -m "Ready for Heroku deployment"
git push heroku main
```

### Step 9: Run Migrations
```bash
heroku run python manage.py migrate
```

### Step 10: Create Superuser
```bash
heroku run python manage.py createsuperuser
```

### Step 11: Collect Static Files
```bash
heroku run python manage.py collectstatic --noinput
```

### Step 12: Open App
```bash
heroku open
```

## 🌐 Alternative: PythonAnywhere

### Steps for PythonAnywhere:
1. Upload code to PythonAnywhere
2. Create virtual environment
3. Install requirements
4. Configure WSGI file
5. Set up static files
6. Configure database

## 📋 Post-Deployment Checklist
- [ ] Test all pages load correctly
- [ ] Test user registration/login
- [ ] Test ordering process
- [ ] Test payment flow
- [ ] Test admin dashboard
- [ ] Check mobile responsiveness
- [ ] Verify SSL certificate
- [ ] Set up domain (if custom domain)
