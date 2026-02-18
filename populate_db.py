import os
import django
from django.conf import settings

# Setup Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'DineAt.settings')
django.setup()

from django.contrib.auth import get_user_model
from apps.orders.models import MenuItem

User = get_user_model()

def populate_db():
    print("Starting database population...")

    # Create Users
    # 1. Admin
    if not User.objects.filter(username='admin').exists():
        admin = User.objects.create_superuser('admin', 'admin@example.com', 'admin123')
        admin.role = User.UserRole.ADMIN
        admin.save()
        print("Superuser 'admin' created.")
    else:
        print("Superuser 'admin' already exists.")

    # 2. Kitchen Staff
    if not User.objects.filter(username='kitchen').exists():
        kitchen = User.objects.create_user('kitchen', 'kitchen@example.com', 'kitchen123')
        kitchen.role = User.UserRole.KITCHEN
        kitchen.save()
        print("Kitchen staff 'kitchen' created.")
    else:
        print("Kitchen staff 'kitchen' already exists.")

    # 3. Customer
    if not User.objects.filter(username='customer').exists():
        customer = User.objects.create_user('customer', 'customer@example.com', 'customer123')
        customer.role = User.UserRole.CUSTOMER
        customer.save()
        print("Customer 'customer' created.")
    else:
        print("Customer 'customer' already exists.")

    # Create Menu Items
    # Using DishType choices from MenuItem model: APPETIZER, MAIN_COURSE, DESSERT, BEVERAGE, SPECIAL
    items = [
        {
            'name': 'Paneer Butter Masala',
            'description': 'Rich and creamy curry with cottage cheese.',
            'price': 280.00,
            'category': MenuItem.DishType.MAIN_COURSE,
            'is_vegetarian': True,
            'is_available': True
        },
        {
            'name': 'Chicken Biryani',
            'description': 'Aromatic rice dish with tender chicken.',
            'price': 320.00,
            'category': MenuItem.DishType.MAIN_COURSE,
            'is_vegetarian': False,
            'is_available': True
        },
        {
            'name': 'Mango Lassi',
            'description': 'Refreshing yogurt-based mango drink.',
            'price': 120.00,
            'category': MenuItem.DishType.BEVERAGE,
            'is_vegetarian': True,
            'is_available': True
        },
         {
            'name': 'Vegetable Samosa',
            'description': 'Crispy pastry filled with spiced potatoes.',
            'price': 50.00,
            'category': MenuItem.DishType.APPETIZER,
            'is_vegetarian': True,
            'is_available': True
        },
        {
            'name': 'Chocolate Brownie',
            'description': 'Warm chocolate brownie with vanilla ice cream.',
            'price': 180.00,
            'category': MenuItem.DishType.DESSERT,
            'is_vegetarian': False, # Contains egg usually
            'is_available': True
        }
    ]

    for item_data in items:
        if not MenuItem.objects.filter(name=item_data['name']).exists():
            MenuItem.objects.create(**item_data)
            print(f"Menu item '{item_data['name']}' created.")
        else:
            print(f"Menu item '{item_data['name']}' already exists.")

    print("Database population completed.")

if __name__ == '__main__':
    populate_db()
