#!/usr/bin/env python
"""
Create test menu items and order for testing payment page
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
from apps.orders.models import MenuItem, Order, OrderItem

def create_test_data():
    """Create test menu items and order"""
    
    print("🍽️ Creating test menu items...")
    
    # Create test menu items
    menu_items_data = [
        {
            'name': 'Butter Chicken',
            'description': 'Tender chicken in rich butter gravy',
            'price': 280,
            'category': 'Main Course',
            'is_vegetarian': False,
            'is_available': True
        },
        {
            'name': 'Paneer Tikka',
            'description': 'Grilled cottage cheese with spices',
            'price': 220,
            'category': 'Main Course',
            'is_vegetarian': True,
            'is_available': True
        },
        {
            'name': 'Veg Fried Rice',
            'description': 'Fried rice with mixed vegetables',
            'price': 150,
            'category': 'Main Course',
            'is_vegetarian': True,
            'is_available': True
        }
    ]
    
    created_items = []
    for item_data in menu_items_data:
        item, created = MenuItem.objects.get_or_create(
            name=item_data['name'],
            defaults=item_data
        )
        if created:
            print(f"✅ Created menu item: {item.name}")
        else:
            print(f"📋 Menu item already exists: {item.name}")
        created_items.append(item)
    
    # Get customer user
    try:
        customer = CustomUser.objects.get(username='customer')
        print(f"✅ Found customer: {customer.username}")
    except CustomUser.DoesNotExist:
        print("❌ Customer user not found!")
        return
    
    # Create test order
    print("\n🛒 Creating test order...")
    
    # Get or create pending order
    cart_order, created = Order.objects.get_or_create(
        customer=customer,
        status=Order.OrderStatus.PENDING
    )
    
    if created:
        print("✅ Created new order")
    else:
        # Clear existing items
        cart_order.items.all().delete()
        print("🔄 Cleared existing order items")
    
    # Add items to order
    for i, menu_item in enumerate(created_items[:2]):  # Add first 2 items
        order_item = OrderItem.objects.create(
            order=cart_order,
            menu_item=menu_item,
            quantity=1,
            price=menu_item.price
        )
        print(f"✅ Added {menu_item.name} to order")
    
    # Calculate total
    total = sum(item.menu_item.price * item.quantity for item in cart_order.items.all())
    print(f"\n💰 Order Total: ₹{total}")
    print(f"📦 Items in order: {cart_order.items.count()}")
    
    print("\n🎯 Test Data Ready!")
    print("🔗 You can now test the payment page:")
    print("1. Login as customer (username: customer, password: customer123)")
    print("2. Add items to cart from menu")
    print("3. Go to payment page to see real-time order data")

if __name__ == '__main__':
    create_test_data()
