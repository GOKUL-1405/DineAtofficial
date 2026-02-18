import os
import django

# Set up Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'DineAt.settings')
django.setup()

from apps.orders.models import Table

# Create tables
tables_data = [
    {'table_number': 1, 'capacity': 2, 'is_available': True},
    {'table_number': 2, 'capacity': 2, 'is_available': True},
    {'table_number': 3, 'capacity': 4, 'is_available': True},
    {'table_number': 4, 'capacity': 4, 'is_available': True},
    {'table_number': 5, 'capacity': 6, 'is_available': True},
    {'table_number': 6, 'capacity': 6, 'is_available': True},
    {'table_number': 7, 'capacity': 8, 'is_available': True},
    {'table_number': 8, 'capacity': 8, 'is_available': True},
]

print("Creating tables...")
for table_data in tables_data:
    table, created = Table.objects.get_or_create(
        table_number=table_data['table_number'],
        defaults=table_data
    )
    if created:
        print(f"Created Table {table.table_number} ({table.capacity} seats)")
    else:
        print(f"Table {table.table_number} already exists")

print(f"\nTotal tables in database: {Table.objects.count()}")
print("Available tables:")
for table in Table.objects.filter(is_available=True):
    print(f"  - Table {table.table_number}: {table.capacity} seats")
