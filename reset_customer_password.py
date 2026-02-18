#!/usr/bin/env python
"""
Reset customer password to known value
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

def reset_customer_password():
    """Reset customer password to known value"""
    
    try:
        # Get customer user
        customer = CustomUser.objects.get(username='customer')
        
        # Set password
        customer.set_password('customer123')
        customer.save()
        
        print("✅ Customer password reset successfully!")
        print(f"👤 Username: {customer.username}")
        print(f"🔑 New Password: customer123")
        print(f"📧 Email: {customer.email}")
        print(f"👥 Role: {customer.get_role_display()}")
        print("\n🔗 Login URL: http://127.0.0.1:8000/accounts/login/customer/")
        print("\n🎯 You can now login with these credentials!")
        
    except CustomUser.DoesNotExist:
        print("❌ Customer user not found! Creating new one...")
        
        # Create new customer user
        customer = CustomUser.objects.create_user(
            username='customer',
            email='customer@dineat.com',
            password='customer123',
            role='CUSTOMER'
        )
        
        print("✅ New customer user created!")
        print(f"👤 Username: {customer.username}")
        print(f"🔑 Password: customer123")
        print(f"📧 Email: {customer.email}")
        print(f"👥 Role: {customer.get_role_display()}")
        print("\n🔗 Login URL: http://127.0.0.1:8000/accounts/login/customer/")
        
    except Exception as e:
        print(f"❌ Error: {e}")

if __name__ == '__main__':
    reset_customer_password()
