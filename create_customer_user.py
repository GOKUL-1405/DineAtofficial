#!/usr/bin/env python
"""
Create a test customer user for DineAt
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

def create_test_customer():
    """Create a test customer user"""
    
    # Check if user already exists
    if CustomUser.objects.filter(username='customer').exists():
        print("✅ Customer user 'customer' already exists!")
        return
    
    try:
        # Create customer user
        user = CustomUser.objects.create_user(
            username='customer',
            email='customer@dineat.com',
            password='customer123',
            role='CUSTOMER',
            phone_number='9876543210'
        )
        
        print(f"✅ Customer user created successfully!")
        print(f"📝 Username: {user.username}")
        print(f"📧 Email: {user.email}")
        print(f"📱 Phone: {user.phone_number}")
        print(f"👤 Role: {user.get_role_display()}")
        print(f"🔑 Password: customer123")
        print("\n🔗 You can now login at: http://127.0.0.1:8000/accounts/login/customer/")
        
    except Exception as e:
        print(f"❌ Error creating customer user: {e}")

if __name__ == '__main__':
    create_test_customer()
