from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from apps.orders.models import Order, MenuItem, Table
from apps.accounts.models import CustomUser
from django.db.models import Count, Sum
from django.utils import timezone
from datetime import timedelta


@login_required
def admin_dashboard_view(request):
    """Admin dashboard with overview and management"""
    
    # Check if user is admin
    if not request.user.is_admin():
        messages.error(request, 'Access denied. Admin privileges required.')
        return redirect('main:index')
    
    # Get statistics
    total_orders = Order.objects.exclude(status=Order.OrderStatus.PENDING).count()
    pending_orders = Order.objects.filter(status=Order.OrderStatus.CONFIRMED).count()
    active_orders = Order.objects.filter(
        status__in=[Order.OrderStatus.PREPARING, Order.OrderStatus.READY]
    ).count()
    
    # Recent orders
    recent_orders = Order.objects.exclude(
        status=Order.OrderStatus.PENDING
    ).select_related('customer', 'table').prefetch_related('items')[:10]
    
    # Revenue statistics
    today = timezone.now().date()
    today_revenue = Order.objects.filter(
        created_at__date=today,
        status=Order.OrderStatus.COMPLETED
    ).aggregate(total=Sum('total_amount'))['total'] or 0
    
    # Popular items
    popular_items = MenuItem.objects.annotate(
        order_count=Count('order_items')
    ).order_by('-order_count')[:5]
    
    # User statistics
    total_customers = CustomUser.objects.filter(role=CustomUser.UserRole.CUSTOMER).count()
    total_staff = CustomUser.objects.filter(role=CustomUser.UserRole.KITCHEN).count()
    
    context = {
        'total_orders': total_orders,
        'pending_orders': pending_orders,
        'active_orders': active_orders,
        'recent_orders': recent_orders,
        'today_revenue': today_revenue,
        'popular_items': popular_items,
        'total_customers': total_customers,
        'total_staff': total_staff,
    }
    
    return render(request, 'dashboard/admin-dashboard.html', context)


@login_required
def admin_order_detail_view(request, order_id):
    """Admin-only order detail view"""

    if not request.user.is_admin():
        messages.error(request, 'Access denied. Admin privileges required.')
        return redirect('main:index')

    order = get_object_or_404(
        Order.objects.exclude(status=Order.OrderStatus.PENDING).select_related('customer', 'table').prefetch_related('items__menu_item'),
        id=order_id,
    )

    context = {
        'order': order,
        'order_items': order.items.all(),
    }

    return render(request, 'dashboard/admin-order-detail.html', context)


@login_required
def admin_order_invoice_view(request, order_id):
    """Admin-only order invoice view"""

    if not request.user.is_admin():
        messages.error(request, 'Access denied. Admin privileges required.')
        return redirect('main:index')

    order = get_object_or_404(
        Order.objects.exclude(status=Order.OrderStatus.PENDING).select_related('customer', 'table').prefetch_related('items__menu_item'),
        id=order_id,
    )

    context = {
        'order': order,
        'order_items': order.items.all(),
    }

    return render(request, 'dashboard/admin-order-invoice.html', context)


@login_required
def kitchen_dashboard_view(request):
    """Kitchen staff dashboard for order management"""
    
    # Check if user is kitchen staff
    if not request.user.is_kitchen_staff():
        messages.error(request, 'Access denied. Kitchen staff privileges required.')
        return redirect('main:index')
    
    # Get active orders
    pending_orders = Order.objects.filter(
        status=Order.OrderStatus.CONFIRMED
    ).select_related('customer', 'table').prefetch_related('items__menu_item')
    
    preparing_orders = Order.objects.filter(
        status=Order.OrderStatus.PREPARING
    ).select_related('customer', 'table').prefetch_related('items__menu_item')
    
    ready_orders = Order.objects.filter(
        status=Order.OrderStatus.READY
    ).select_related('customer', 'table').prefetch_related('items__menu_item')
    
    context = {
        'pending_orders': pending_orders,
        'preparing_orders': preparing_orders,
        'ready_orders': ready_orders,
    }
    
    return render(request, 'dashboard/kitchen-dashboard.html', context)


@login_required
def update_order_status(request, order_id):
    """Update order status (kitchen staff only)"""
    
    if not request.user.is_kitchen_staff() and not request.user.is_admin():
        messages.error(request, 'Access denied.')
        return redirect('main:index')
    
    if request.method == 'POST':
        order = get_object_or_404(Order, id=order_id)
        new_status = request.POST.get('status')
        
        if new_status in dict(Order.OrderStatus.choices):
            order.status = new_status
            order.save()
            messages.success(request, f'Order #{order.id} status updated to {order.get_status_display()}')
        else:
            messages.error(request, 'Invalid status.')
    
    # Redirect based on user role
    if request.user.is_kitchen_staff():
        return redirect('dashboard:kitchen_dashboard')
    else:
        return redirect('dashboard:admin_dashboard')


@login_required
def clear_recent_orders(request):
    """Clear all recent orders from the system"""
    
    # Check if user is admin
    if not request.user.is_admin():
        messages.error(request, 'Access denied. Admin privileges required.')
        return redirect('main:index')
    
    if request.method == 'POST':
        # Delete all orders except pending ones
        deleted_count = Order.objects.exclude(
            status=Order.OrderStatus.PENDING
        ).delete()[0]
        
        messages.success(request, f'Successfully cleared {deleted_count} recent orders from the system.')
    
    return redirect('dashboard:admin_dashboard')


from django.http import JsonResponse
from django.core.cache import cache


@login_required
def admin_stats_api(request):
    """API endpoint for real-time dashboard stats"""
    
    # Check if user is admin
    if not request.user.is_admin():
        return JsonResponse({'error': 'Access denied'}, status=403)
    
    # Get current stats
    total_orders = Order.objects.exclude(status=Order.OrderStatus.PENDING).count()
    pending_orders = Order.objects.filter(status=Order.OrderStatus.CONFIRMED).count()
    active_orders = Order.objects.filter(
        status__in=[Order.OrderStatus.PREPARING, Order.OrderStatus.READY]
    ).count()
    
    # Calculate today's revenue
    today = timezone.now().date()
    today_revenue = Order.objects.filter(
        created_at__date=today,
        status__in=[Order.OrderStatus.CONFIRMED, Order.OrderStatus.PREPARING, 
                   Order.OrderStatus.READY, Order.OrderStatus.COMPLETED]
    ).aggregate(total=Sum('total_amount'))['total'] or 0
    
    # Get previous stats from cache to detect new orders
    cache_key = f'admin_stats_{request.user.id}'
    previous_stats = cache.get(cache_key, {})
    
    # Calculate new orders since last check
    new_orders = max(0, total_orders - previous_stats.get('total_orders', 0))
    
    # Update cache
    current_stats = {
        'total_orders': total_orders,
        'pending_orders': pending_orders,
        'active_orders': active_orders,
        'today_revenue': today_revenue
    }
    cache.set(cache_key, current_stats, 300)  # Cache for 5 minutes
    
    return JsonResponse({
        'total_orders': total_orders,
        'pending_orders': pending_orders,
        'active_orders': active_orders,
        'today_revenue': today_revenue,
        'new_orders': new_orders
    })
