import google.generativeai as genai
from django.conf import settings
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
import json
from decouple import config

# Project Information - Comprehensive Description
PROJECT_INFO = """
DINEAT RESTAURANT MANAGEMENT SYSTEM - COMPLETE PROJECT OVERVIEW

PROJECT STRUCTURE:
- Django-based web application for restaurant management
- Multi-role system: Admin, Kitchen Staff, Customers
- Real-time order processing and table management
- Complete payment integration with multiple methods

CORE FEATURES:

1. CUSTOMER-FACING FEATURES:
   - Menu browsing with categories (Vegetarian, Non-vegetarian, Appetizers, Main Course, Desserts, Beverages)
   - Real-time cart management with add/remove/update functionality
   - Table selection and reservation system
   - Multiple payment options: COD, Credit/Debit Cards, UPI (GPay, PhonePe, Paytm), Digital Wallets
   - Order tracking with real-time status updates
   - Contact page with social media integration
   - Help and support system

2. KITCHEN STAFF FEATURES:
   - Real-time order dashboard showing incoming orders
   - Order status management (Pending, Preparing, Ready, Completed)
   - Queue management and order prioritization
   - Order details with customer information and table numbers
   - Preparation time tracking

3. ADMIN FEATURES:
   - Comprehensive dashboard with real-time statistics
   - Order management with filtering and search capabilities
   - Revenue tracking and analytics
   - User management and role assignments
   - Database management (clear orders, backup, restore)
   - System configuration and settings

TECHNICAL ARCHITECTURE:

BACKEND:
- Django 5.0 framework
- MySQL database with optimized ORM queries
- Role-based authentication system
- RESTful API design patterns
- Secure form handling with CSRF protection
- Session management and user authentication

FRONTEND:
- Responsive design with mobile support
- Modern UI with gradient backgrounds and animations
- JavaScript-based real-time updates
- Hamburger menu for mobile navigation
- Toast notifications for user feedback
- Interactive components and smooth transitions

DATABASE MODELS:
- User model with role-based permissions (Admin, Kitchen Staff, Customer)
- Order model with status tracking and timestamps
- Menu item model with categories and pricing
- Table model with availability status
- Cart model for temporary order storage

KEY PAGES AND FUNCTIONALITY:

1. HOME PAGE (main:index):
   - Restaurant overview and welcome message
   - Navigation to all major sections
   - Featured items and promotions

2. MENU PAGE (orders:menu):
   - Categorized food items display
   - Add to cart functionality with real-time updates
   - Item details with prices and descriptions
   - Vegetarian/Non-vegetarian indicators

3. CART PAGE (orders:cart):
   - Real-time cart display with item management
   - Quantity controls and item removal
   - Total calculation and summary
   - Proceed to payment functionality

4. PAYMENT PAGE (main:payment):
   - Two-column layout with order details and payment options
   - Multiple payment method selection
   - QR code generation for UPI payments
   - Secure payment processing simulation

5. KITCHEN DASHBOARD (dashboard:kitchen):
   - Real-time order queue display
   - Order status update interface
   - Preparation time tracking
   - Order filtering and search

6. ADMIN DASHBOARD (dashboard:admin):
   - Comprehensive statistics and analytics
   - Revenue tracking with charts
   - Order management interface
   - User management system

SECURITY FEATURES:
- CSRF protection on all forms
- Role-based access control
- Input validation and sanitization
- Secure password handling
- Session security management

INTEGRATION FEATURES:
- Social media links (Instagram, LinkedIn, YouTube)
- Payment gateway integration
- Email notification system
- Real-time chatbot support
- Help and documentation system

MOBILE RESPONSIVENESS:
- Fully responsive design for all screen sizes
- Touch-friendly interface elements
- Optimized navigation for mobile devices
- Adaptive layouts and components

PERFORMANCE OPTIMIZATIONS:
- Database query optimization with select_related and prefetch_related
- Static file compression and caching
- Efficient template rendering
- Minimal JavaScript for fast loading

DEPLOYMENT READY:
- Environment configuration support
- Production-ready settings
- Database migration scripts
- Comprehensive documentation

The system provides a complete restaurant management solution with customer ordering, kitchen operations, and administrative control in a single integrated platform.
"""

# Initialize Gemini AI
def initialize_gemini():
    try:
        api_key = config('GEMINI_API_KEY', default='AIzaSyAFeKBgVblp0KDlbAiTSs2AOuEOvvaH0IM')
        if not api_key:
            return None
    
        genai.configure(api_key=api_key)
        model = genai.GenerativeModel('models/gemini-2.5-flash')
        return model
    except Exception as e:
        print(f"Error initializing Gemini: {e}")
        return None

# Initialize the model
gemini_model = initialize_gemini()

@csrf_exempt
@require_http_methods(["POST"])
def chatbot_query(request):
    """
    Handle chatbot queries with Gemini AI integration
    """
    if not gemini_model:
        return JsonResponse({
            'error': 'Chatbot service is not available. Please configure Gemini API key.'
        }, status=500)
    
    try:
        # Parse request data
        data = json.loads(request.body)
        user_message = data.get('message', '').strip()
        
        if not user_message:
            return JsonResponse({
                'error': 'Message is required'
            }, status=400)
        
        # Create the prompt for Gemini
        prompt = f"""You are a chatbot for a specific software project.

Project details:
{PROJECT_INFO}

Rules:
- Answer only from project details
- Do not use external knowledge
- If unrelated question, say it is outside project scope
- Be helpful and concise
- Provide specific information about the DineAt Restaurant Management System

User question: {user_message}

Provide a helpful response based only on the project information above."""
        
        # Get response from Gemini
        response = gemini_model.generate_content(prompt)
        bot_response = response.text
        
        # Check if the response indicates the question is outside scope
        if "outside project scope" in bot_response.lower() or "not related" in bot_response.lower():
            bot_response = "This question is outside the project scope."
        
        return JsonResponse({
            'response': bot_response,
            'status': 'success'
        })
        
    except json.JSONDecodeError:
        return JsonResponse({
            'error': 'Invalid JSON format'
        }, status=400)
        
    except Exception as e:
        return JsonResponse({
            'error': f'An error occurred: {str(e)}'
        }, status=500)

@csrf_exempt
@require_http_methods(["GET"])
def chatbot_status(request):
    """
    Check if chatbot is available
    """
    return JsonResponse({
        'status': 'available' if gemini_model else 'unavailable',
        'message': 'Chatbot is ready' if gemini_model else 'Gemini API not configured'
    })
