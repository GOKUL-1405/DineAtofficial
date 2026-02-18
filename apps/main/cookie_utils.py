"""
Cookie utilities for DineAt website
"""

from django.http import HttpResponse
from django.conf import settings
import json
from datetime import datetime, timedelta


def set_cookie(response, key, value, days_expire=7):
    """
    Set a cookie with expiration
    """
    if isinstance(value, (dict, list)):
        value = json.dumps(value)
    
    expires = datetime.utcnow() + timedelta(days=days_expire)
    response.set_cookie(
        key,
        value,
        expires=expires,
        httponly=True,
        secure=settings.DEBUG is False,  # Use secure in production
        samesite='Lax'
    )
    return response


def get_cookie(request, key, default=None):
    """
    Get cookie value and parse JSON if needed
    """
    cookie_value = request.COOKIES.get(key, default)
    
    if cookie_value and cookie_value != default:
        try:
            # Try to parse as JSON
            return json.loads(cookie_value)
        except (json.JSONDecodeError, TypeError):
            # Return as string if not JSON
            return cookie_value
    
    return default


def delete_cookie(response, key):
    """
    Delete a cookie
    """
    response.delete_cookie(key)
    return response


def set_user_preferences(response, preferences):
    """
    Set user preferences cookie
    """
    return set_cookie(response, 'user_preferences', preferences, days_expire=30)


def get_user_preferences(request):
    """
    Get user preferences from cookie
    """
    return get_cookie(request, 'user_preferences', {})


def set_cart_cookie(response, cart_data):
    """
    Set cart data in cookie for persistence
    """
    return set_cookie(response, 'cart_data', cart_data, days_expire=1)


def get_cart_cookie(request):
    """
    Get cart data from cookie
    """
    return get_cookie(request, 'cart_data', [])


def set_theme_cookie(response, theme):
    """
    Set theme preference cookie
    """
    return set_cookie(response, 'theme', theme, days_expire=30)


def get_theme_cookie(request):
    """
    Get theme preference from cookie
    """
    return get_cookie(request, 'theme', 'light')


def set_language_cookie(response, language):
    """
    Set language preference cookie
    """
    return set_cookie(response, 'language', language, days_expire=30)


def get_language_cookie(request):
    """
    Get language preference from cookie
    """
    return get_cookie(request, 'language', 'en')


def set_table_preference(response, table_number):
    """
    Set table preference cookie
    """
    return set_cookie(response, 'preferred_table', table_number, days_expire=1)


def get_table_preference(request):
    """
    Get table preference from cookie
    """
    return get_cookie(request, 'preferred_table', None)
