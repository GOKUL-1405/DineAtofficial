from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Sum, Count
from django.utils import timezone
from .models import CustomUser, CustomerProfile
from apps.orders.models import Order


def login_view(request):
    """General login page - redirects to role-specific login"""
    return render(request, 'accounts/login.html')


def admin_login_view(request):
    """Admin login page"""
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        
        user = authenticate(request, username=username, password=password)
        
        if user is not None and user.is_admin():
            login(request, user)
            messages.success(request, f'Welcome back, {user.username}!')
            return redirect('dashboard:admin_dashboard')
        else:
            messages.error(request, 'Invalid credentials or insufficient permissions.')
    
    return render(request, 'accounts/admin-login.html')


def kitchen_login_view(request):
    """Kitchen staff login page"""
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        
        user = authenticate(request, username=username, password=password)
        
        if user is not None and user.is_kitchen_staff():
            login(request, user)
            messages.success(request, f'Welcome back, {user.username}!')
            return redirect('dashboard:kitchen_dashboard')
        else:
            messages.error(request, 'Invalid credentials or insufficient permissions.')
    
    return render(request, 'accounts/kitchen-login.html')


def customer_login_view(request):
    """Customer login page"""
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        
        user = authenticate(request, username=username, password=password)
        
        if user is not None and user.is_customer():
            login(request, user)
            messages.success(request, f'Welcome back, {user.username}!')
            return redirect('orders:table_selection')
        else:
            messages.error(request, 'Invalid credentials or insufficient permissions.')
    
    return render(request, 'accounts/customer-login.html')


def customer_signup_view(request):
    """Customer signup page"""
    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')
        confirm_password = request.POST.get('confirm_password')
        phone_number = request.POST.get('phone_number')

        if password != confirm_password:
            messages.error(request, 'Passwords do not match.')
            return render(request, 'accounts/customer-signup.html')
        
        if CustomUser.objects.filter(username=username).exists():
            messages.error(request, 'Username already exists.')
            return render(request, 'accounts/customer-signup.html')

        if CustomUser.objects.filter(email=email).exists():
            messages.error(request, 'Email already exists.')
            return render(request, 'accounts/customer-signup.html')

        user = CustomUser.objects.create_user(username=username, email=email, password=password)
        user.phone_number = phone_number
        user.role = CustomUser.UserRole.CUSTOMER
        user.save()

        login(request, user)
        messages.success(request, f'Account created successfully! Welcome, {user.username}!')
        return redirect('orders:table_selection')
        
    return render(request, 'accounts/customer-signup.html')


@login_required
def logout_view(request):
    """Logout user and redirect to home"""
    logout(request)
    messages.info(request, 'You have been logged out successfully.')
    return redirect('main:index')


@login_required
def profile_view(request):
    """Customer profile view"""
    if not request.user.is_customer():
        messages.error(request, 'Access denied. This page is for customers only.')
        return redirect('main:index')
    
    # Get or create customer profile
    profile, created = CustomerProfile.objects.get_or_create(user=request.user)
    
    # Get order history
    orders = Order.objects.filter(customer=request.user).order_by('-created_at')[:10]
    
    # Calculate statistics
    total_orders = Order.objects.filter(customer=request.user).count()
    total_spent = Order.objects.filter(customer=request.user).aggregate(
        total=Sum('total_amount')
    )['total'] or 0
    
    context = {
        'profile': profile,
        'orders': orders,
        'total_orders': total_orders,
        'total_spent': total_spent,
    }
    
    return render(request, 'accounts/profile.html', context)


@login_required
def edit_profile_view(request):
    """Edit customer profile"""
    if not request.user.is_customer():
        messages.error(request, 'Access denied. This page is for customers only.')
        return redirect('main:index')
    
    profile, created = CustomerProfile.objects.get_or_create(user=request.user)
    
    if request.method == 'POST':
        # Update personal information
        profile.first_name = request.POST.get('first_name', '')
        profile.last_name = request.POST.get('last_name', '')
        profile.phone_number = request.POST.get('phone_number', '')
        
        # Update address
        profile.address_line1 = request.POST.get('address_line1', '')
        profile.address_line2 = request.POST.get('address_line2', '')
        profile.city = request.POST.get('city', '')
        profile.state = request.POST.get('state', '')
        profile.postal_code = request.POST.get('postal_code', '')
        profile.country = request.POST.get('country', 'India')
        
        # Update preferences
        profile.preferred_language = request.POST.get('preferred_language', 'en')
        profile.dietary_preferences = request.POST.get('dietary_preferences', '')
        profile.food_allergies = request.POST.get('food_allergies', '')
        
        # Update notification preferences
        profile.email_notifications = request.POST.get('email_notifications') == 'on'
        profile.sms_notifications = request.POST.get('sms_notifications') == 'on'
        profile.promotional_emails = request.POST.get('promotional_emails') == 'on'
        
        # Handle profile picture upload
        if 'profile_picture' in request.FILES:
            profile.profile_picture = request.FILES['profile_picture']
        
        # Handle date of birth
        dob = request.POST.get('date_of_birth')
        if dob:
            try:
                profile.date_of_birth = timezone.datetime.strptime(dob, '%Y-%m-%d').date()
            except ValueError:
                messages.error(request, 'Invalid date format for date of birth.')
        
        try:
            profile.save()
            
            # Update user phone number if provided
            if request.POST.get('phone_number'):
                request.user.phone_number = request.POST.get('phone_number')
                request.user.save()
            
            messages.success(request, 'Profile updated successfully!')
            return redirect('accounts:profile')
        except Exception as e:
            messages.error(request, f'Error updating profile: {str(e)}')
    
    context = {
        'profile': profile,
    }
    
    return render(request, 'accounts/edit_profile.html', context)


@login_required
def order_history_view(request):
    """Customer order history"""
    if not request.user.is_customer():
        messages.error(request, 'Access denied. This page is for customers only.')
        return redirect('main:index')
    
    orders = Order.objects.filter(customer=request.user).order_by('-created_at')
    
    context = {
        'orders': orders,
    }
    
    return render(request, 'accounts/order_history.html', context)
