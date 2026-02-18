#!/usr/bin/env python
"""
Show existing users in DineAt database
"""

import os
import sys
import django

# Add project directory to Python path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# Set up Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'DineAt.settings')
django.setup()

from apps.accounts.models import CustomUser

def show_users():
    """Display all users in the database"""
    
    print("📋 DineAt Users:")
    print("=" * 50)
    
    users = CustomUser.objects.all()
    
    if not users:
        print("❌ No users found in database!")
        return
    
    for user in users:
        print(f"👤 Username: {user.username}")
        print(f"📧 Email: {user.email}")
        print(f"📱 Phone: {user.phone_number or 'Not set'}")
        print(f"👥 Role: {user.get_role_display()}")
        print(f"📅 Created: {user.created_at.strftime('%Y-%m-%d %H:%M')}")
        print(f"🔑 Password: [Hidden for security]")
        print("-" * 50)
        
        # Show customer login info specifically
        if user.is_customer():
            print("🏠 CUSTOMER LOGIN CREDENTIALS:")
            print(f"   Username: {user.username}")
            print(f"   Password: customer123 (if you created using script)")
            print("-" * 50)

if __name__ == '__main__':
    show_users()
