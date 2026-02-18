from django.contrib import admin
from .models import MenuItem, Table, Order, OrderItem


class OrderItemInline(admin.TabularInline):
    """Inline display of order items within order admin"""
    model = OrderItem
    extra = 0
    readonly_fields = ['subtotal']
    
    def subtotal(self, obj):
        return f"₹{obj.subtotal}"
    subtotal.short_description = 'Subtotal'


@admin.register(MenuItem)
class MenuItemAdmin(admin.ModelAdmin):
    """Admin interface for menu items"""
    list_display = ['name', 'category', 'price', 'is_available', 'is_vegetarian', 'preparation_time']
    list_filter = ['category', 'is_available', 'is_vegetarian', 'is_vegan']
    search_fields = ['name', 'description']
    list_editable = ['is_available', 'price']
    ordering = ['category', 'name']


@admin.register(Table)
class TableAdmin(admin.ModelAdmin):
    """Admin interface for tables"""
    list_display = ['table_number', 'capacity', 'is_available']
    list_filter = ['is_available', 'capacity']
    list_editable = ['is_available']
    ordering = ['table_number']


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    """Admin interface for orders"""
    list_display = ['id', 'customer', 'table', 'status', 'total_amount', 'created_at']
    list_filter = ['status', 'created_at']
    search_fields = ['customer__username', 'id']
    readonly_fields = ['created_at', 'updated_at', 'total_amount']
    inlines = [OrderItemInline]
    list_editable = ['status']
    ordering = ['-created_at']
    
    fieldsets = (
        ('Order Information', {
            'fields': ('customer', 'table', 'status')
        }),
        ('Financial', {
            'fields': ('total_amount',)
        }),
        ('Additional Details', {
            'fields': ('special_instructions',)
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )


@admin.register(OrderItem)
class OrderItemAdmin(admin.ModelAdmin):
    """Admin interface for order items"""
    list_display = ['order', 'menu_item', 'quantity', 'price', 'get_subtotal']
    list_filter = ['order__status']
    search_fields = ['order__id', 'menu_item__name']
    
    def get_subtotal(self, obj):
        return f"₹{obj.subtotal}"
    get_subtotal.short_description = 'Subtotal'
