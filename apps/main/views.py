from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse, HttpResponse
from apps.orders.models import MenuItem, Order
from .cookie_utils import set_user_preferences, get_user_preferences, set_theme_cookie, get_theme_cookie
import json


def index_view(request):
    """Homepage with cookie support"""
    featured_items = MenuItem.objects.filter(is_available=True)[:6]
    
    # Get user preferences from cookies
    user_prefs = get_user_preferences(request)
    theme = get_theme_cookie(request)
    
    context = {
        'featured_items': featured_items,
        'user_preferences': user_prefs,
        'theme': theme,
        'welcome_message': user_prefs.get('welcome_message', 'Welcome to DineAt!')
    }
    
    response = render(request, 'main/index.html', context)
    
    # Set theme cookie if not exists
    if not request.COOKIES.get('theme'):
        response = set_theme_cookie(response, 'light')
    
    return response


def about_view(request):
    """About page with cookie support"""
    user_prefs = get_user_preferences(request)
    theme = get_theme_cookie(request)
    
    context = {
        'user_preferences': user_prefs,
        'theme': theme
    }
    
    return render(request, 'main/about.html', context)


def contact_view(request):
    """Contact page with cookie support"""
    user_prefs = get_user_preferences(request)
    theme = get_theme_cookie(request)
    
    context = {
        'user_preferences': user_prefs,
        'theme': theme
    }
    
    return render(request, 'main/contact.html', context)


def help_view(request):
    """Help/FAQ page with cookie support"""
    user_prefs = get_user_preferences(request)
    theme = get_theme_cookie(request)
    
    context = {
        'user_preferences': user_prefs,
        'theme': theme
    }
    
    return render(request, 'main/help.html', context)


@login_required
def payment_view(request):
    """Payment page with real-time order data and cookie support"""
    
    # Get real-time order data from database
    # Get or create pending order for current user
    cart_order, created = Order.objects.get_or_create(
        customer=request.user,
        status=Order.OrderStatus.PENDING
    )
    
    # Get order items
    order_items = []
    total_amount = 0
    
    for item in cart_order.items.all():
        order_items.append({
            'name': item.menu_item.name,
            'price': item.menu_item.price,
            'quantity': item.quantity
        })
        total_amount += item.menu_item.price * item.quantity
    
    # Get user preferences
    user_prefs = get_user_preferences(request)
    theme = get_theme_cookie(request)
    
    context = {
        'order_items': order_items,
        'total_amount': total_amount,
        'cart_order': cart_order,
        'user_preferences': user_prefs,
        'theme': theme
    }
    
    return render(request, 'main/payment.html', context)


def save_preferences(request):
    """Save user preferences via AJAX"""
    if request.method == 'POST':
        try:
            preferences = json.loads(request.body)
            
            # Save preferences to cookie
            response = JsonResponse({'success': True, 'message': 'Preferences saved successfully'})
            response = set_user_preferences(response, preferences)
            
            return response
            
        except json.JSONDecodeError:
            return JsonResponse({'success': False, 'message': 'Invalid data format'})
        except Exception as e:
            return JsonResponse({'success': False, 'message': str(e)})
    
    return JsonResponse({'success': False, 'message': 'Invalid request method'})


def toggle_theme(request):
    """Toggle theme between light and dark"""
    if request.method == 'POST':
        current_theme = get_theme_cookie(request)
        new_theme = 'dark' if current_theme == 'light' else 'light'
        
        response = JsonResponse({
            'success': True, 
            'theme': new_theme,
            'message': f'Theme changed to {new_theme}'
        })
        
        response = set_theme_cookie(response, new_theme)
        return response
    
    return JsonResponse({'success': False, 'message': 'Invalid request method'})


def get_cookie_info(request):
    """Get all cookie information for debugging"""
    cookies = {}
    for key, value in request.COOKIES.items():
        cookies[key] = value
    
    return JsonResponse({
        'cookies': cookies,
        'count': len(cookies)
    })


