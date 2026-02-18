import os
import django

# Set up Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'DineAt.settings')
django.setup()

from apps.orders.models import MenuItem

# Create menu items
menu_items_data = [
    # Vegetarian items
    {'name': 'Paneer Tikka', 'description': 'Soft cottage cheese marinated in spices and grilled', 'price': 180, 'is_vegetarian': True, 'category': 'APPETIZER'},
    {'name': 'Vegetable Samosa', 'description': 'Crispy pastry filled with spiced vegetables', 'price': 80, 'is_vegetarian': True, 'category': 'APPETIZER'},
    {'name': 'Dal Makhani', 'description': 'Creamy black lentils cooked with butter and spices', 'price': 220, 'is_vegetarian': True, 'category': 'MAIN_COURSE'},
    {'name': 'Palak Paneer', 'description': 'Cottage cheese in creamy spinach gravy', 'price': 200, 'is_vegetarian': True, 'category': 'MAIN_COURSE'},
    {'name': 'Vegetable Biryani', 'description': 'Fragrant rice with mixed vegetables and spices', 'price': 180, 'is_vegetarian': True, 'category': 'MAIN_COURSE'},
    {'name': 'Gulab Jamun', 'description': 'Soft milk dumplings in sugar syrup', 'price': 60, 'is_vegetarian': True, 'category': 'DESSERT'},
    
    # Non-vegetarian items
    {'name': 'Chicken Tikka', 'description': 'Tender chicken pieces marinated in spices and grilled', 'price': 250, 'is_vegetarian': False, 'category': 'APPETIZER'},
    {'name': 'Fish Fry', 'description': 'Crispy fried fish with spices', 'price': 280, 'is_vegetarian': False, 'category': 'APPETIZER'},
    {'name': 'Butter Chicken', 'description': 'Tender chicken in creamy tomato gravy', 'price': 320, 'is_vegetarian': False, 'category': 'MAIN_COURSE'},
    {'name': 'Chicken Biryani', 'description': 'Fragrant rice with spiced chicken pieces', 'price': 280, 'is_vegetarian': False, 'category': 'MAIN_COURSE'},
    {'name': 'Mutton Rogan Josh', 'description': 'Tender mutton in aromatic Kashmiri spices', 'price': 380, 'is_vegetarian': False, 'category': 'MAIN_COURSE'},
    
    # Beverages
    {'name': 'Fresh Lime Soda', 'description': 'Refreshing lime soda with mint', 'price': 40, 'is_vegetarian': True, 'category': 'BEVERAGE'},
    {'name': 'Mango Lassi', 'description': 'Sweet yogurt drink with mango flavor', 'price': 60, 'is_vegetarian': True, 'category': 'BEVERAGE'},
    {'name': 'Masala Tea', 'description': 'Spiced Indian tea with milk', 'price': 30, 'is_vegetarian': True, 'category': 'BEVERAGE'},
]

print("\nCreating menu items...")
for item_data in menu_items_data:
    menu_item, created = MenuItem.objects.get_or_create(
        name=item_data['name'],
        defaults={
            'description': item_data['description'],
            'price': item_data['price'],
            'is_vegetarian': item_data['is_vegetarian'],
            'category': item_data['category'],
            'is_available': True
        }
    )
    
    if created:
        veg_status = "Veg" if item_data['is_vegetarian'] else "Non-Veg"
        print(f"Created {veg_status} item: {menu_item.name} - ₹{menu_item.price}")
    else:
        print(f"Menu item {item_data['name']} already exists")

print(f"\nTotal menu items: {MenuItem.objects.count()}")
print("Available menu items:")
for item in MenuItem.objects.filter(is_available=True):
    veg_status = "🌱" if item.is_vegetarian else "🥩"
    print(f"  {veg_status} {item.name} - ₹{item.price} ({item.get_category_display()})")
