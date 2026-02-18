from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Q
from django.http import JsonResponse
from django.urls import reverse
from django.core.cache import cache
import uuid
import json
from decimal import Decimal
from .models import MenuItem, Order, OrderItem, Table
from .upi_utils import create_upi_payment_qr, get_upi_payment_info


@login_required
def menu_view(request):
    """Display menu items with filtering"""
    category = request.GET.get('category', '')
    search = request.GET.get('search', '')
    
    menu_items = MenuItem.objects.filter(is_available=True)
    
    if category:
        menu_items = menu_items.filter(category=category)
    
    if search:
        menu_items = menu_items.filter(
            Q(name__icontains=search) | Q(description__icontains=search)
        )
    
    categories = MenuItem.DishType.choices
    
    context = {
        'menu_items': menu_items,
        'categories': categories,
        'selected_category': category,
        'search_query': search,
    }
    
    return render(request, 'orders/menu.html', context)


@login_required
def cart_view(request):
    """Display and manage shopping cart"""
    # Get or create pending order for current user
    cart_order, created = Order.objects.get_or_create(
        customer=request.user,
        status=Order.OrderStatus.PENDING
    )
    
    cart_items = cart_order.items.all()
    
    context = {
        'cart_order': cart_order,
        'cart_items': cart_items,
    }
    
    return render(request, 'orders/cart.html', context)


@login_required
def add_to_cart(request, item_id):
    """Add item to cart"""
    menu_item = get_object_or_404(MenuItem, id=item_id, is_available=True)
    
    # Get or create pending order
    cart_order, created = Order.objects.get_or_create(
        customer=request.user,
        status=Order.OrderStatus.PENDING
    )
    
    # Check if item already in cart
    order_item, created = OrderItem.objects.get_or_create(
        order=cart_order,
        menu_item=menu_item,
        defaults={'quantity': 1, 'price': menu_item.price}
    )
    
    if not created:
        order_item.quantity += 1
        order_item.save()
    
    cart_order.calculate_total()
    messages.success(request, f'{menu_item.name} added to cart!')
    
    return redirect('orders:cart')


@login_required
def remove_from_cart(request, item_id):
    """Remove item from cart"""
    order_item = get_object_or_404(OrderItem, id=item_id, order__customer=request.user)
    order = order_item.order
    order_item.delete()
    order.calculate_total()
    
    messages.info(request, 'Item removed from cart.')
    return redirect('orders:cart')


@login_required
def update_cart_item(request, item_id):
    """Update cart item quantity"""
    if request.method == 'POST':
        order_item = get_object_or_404(OrderItem, id=item_id, order__customer=request.user)
        quantity = int(request.POST.get('quantity', 1))
        
        if quantity > 0:
            order_item.quantity = quantity
            order_item.save()
            order_item.order.calculate_total()
            messages.success(request, 'Cart updated!')
        else:
            order_item.delete()
            order_item.order.calculate_total()
            messages.info(request, 'Item removed from cart.')
    
    return redirect('orders:cart')


@login_required
def table_selection_view(request):
    """Select table for dining"""
    available_tables = Table.objects.filter(is_available=True)
    
    if request.method == 'POST':
        table_id = request.POST.get('table_id')
        table = get_object_or_404(Table, id=table_id, is_available=True)
        
        # Store table selection in session
        request.session['selected_table_id'] = table.id
        messages.success(request, f'Table {table.table_number} selected! Redirecting to menu...')
        return redirect(f'/orders/menu/?table={table.table_number}')
    
    context = {
        'tables': available_tables,
    }
    
    return render(request, 'orders/table-selection.html', context)


@login_required
def order_confirmation_view(request):
    """Confirm and place order"""
    # Try to load the current pending order first
    cart_order = None
    try:
        cart_order = Order.objects.get(
            customer=request.user,
            status=Order.OrderStatus.PENDING
        )
    except Order.DoesNotExist:
        cart_order = None

    if request.method == 'POST':
        if not cart_order:
            messages.error(request, 'Your cart is empty!')
            return redirect('orders:menu')

        cart_data_raw = request.POST.get('cart_data', '')
        if cart_data_raw:
            try:
                cart_data = json.loads(cart_data_raw)
            except json.JSONDecodeError:
                cart_data = None

            if isinstance(cart_data, list):
                cart_order.items.all().delete()
                for cart_item in cart_data:
                    if not isinstance(cart_item, dict):
                        continue

                    name = (cart_item.get('name') or '').strip()
                    if not name:
                        continue

                    try:
                        quantity = int(cart_item.get('quantity', 1))
                    except (TypeError, ValueError):
                        quantity = 1

                    if quantity < 1:
                        continue

                    try:
                        price = Decimal(str(cart_item.get('price', '0')))
                    except Exception:
                        price = Decimal('0.00')

                    menu_item = MenuItem.objects.filter(name=name).first()
                    if not menu_item:
                        menu_item = MenuItem.objects.create(
                            name=name,
                            description=name,
                            price=price if price > 0 else Decimal('0.01'),
                            is_available=True,
                            is_vegetarian=(cart_item.get('category') == 'veg'),
                        )

                    OrderItem.objects.create(
                        order=cart_order,
                        menu_item=menu_item,
                        quantity=quantity,
                        price=price if price > 0 else menu_item.price,
                    )

                cart_order.calculate_total()

        # Get selected table
        table_id = request.session.get('selected_table_id')
        if table_id:
            table = get_object_or_404(Table, id=table_id)
            cart_order.table = table
        
        # Get payment method from form
        payment_method = request.POST.get('payment_method', 'cod')
        cart_order.payment_method = payment_method
        
        # Get special instructions
        cart_order.special_instructions = request.POST.get('special_instructions', '')
        
        # Confirm order
        cart_order.status = Order.OrderStatus.CONFIRMED
        cart_order.save()

        request.session['last_confirmed_order_id'] = cart_order.id
        
        # Clear session
        if 'selected_table_id' in request.session:
            del request.session['selected_table_id']
        
        messages.success(request, f'Order #{cart_order.id} placed successfully!')
        return redirect('orders:order_confirmation')

    if not cart_order:
        last_confirmed_order_id = request.session.get('last_confirmed_order_id')
        if last_confirmed_order_id:
            cart_order = get_object_or_404(Order, id=last_confirmed_order_id, customer=request.user)
        else:
            messages.error(request, 'Your cart is empty!')
            return redirect('orders:menu')
    
    context = {
        'order': cart_order,
        'cart_items': cart_order.items.all(),
    }
    
    return render(request, 'orders/order-confirmation.html', context)


@login_required
def payment_view(request):
    """Separate payment step: show payment options and submit to process_payment_view."""

    if request.method != 'POST':
        messages.error(request, 'Please review your cart before payment.')
        return redirect('orders:cart')

    cart_data = request.POST.get('cart_data', '')
    total_amount = request.POST.get('total_amount', '')

    # Convert total_amount to decimal for UPI payment
    try:
        amount = Decimal(total_amount)
    except (ValueError, TypeError):
        amount = Decimal('0.00')

    token = uuid.uuid4()
    cache.set(
        f"pay:{token}",
        {
            'status': 'pending',
            'cart_data': cart_data,
            'total_amount': total_amount,
            'amount': amount,
        },
        timeout=15 * 60,
    )

    mark_paid_url = request.build_absolute_uri(
        reverse('orders:upi_mark_paid', kwargs={'token': token})
    )

    status_url = reverse('orders:payment_status', kwargs={'token': token})

    # Generate UPI QR code for payment
    upi_payment_info = None
    if amount > 0:
        try:
            # Create a temporary order ID for QR generation
            temp_order_id = f"temp_{int(token)}"
            upi_payment_info = create_upi_payment_qr(float(amount), temp_order_id)
        except Exception as e:
            messages.warning(request, f'UPI QR generation failed: {str(e)}')
            # Fallback to basic UPI info
            upi_payment_info = get_upi_payment_info(float(amount), temp_order_id)

    context = {
        'cart_data': cart_data,
        'total_amount': total_amount,
        'payment_token': token,
        'upi_mark_paid_url': mark_paid_url,
        'payment_status_url': status_url,
        'upi_payment_info': upi_payment_info,
    }

    return render(request, 'orders/payment_simple.html', context)


@login_required
def upi_payment_view(request):
    """Dedicated UPI payment view with QR code generation"""
    
    if request.method != 'POST':
        messages.error(request, 'Please review your cart before payment.')
        return redirect('orders:cart')

    cart_data = request.POST.get('cart_data', '')
    total_amount = request.POST.get('total_amount', '')

    # Convert total_amount to decimal for UPI payment
    try:
        amount = Decimal(total_amount)
    except (ValueError, TypeError):
        amount = Decimal('0.00')

    if amount <= 0:
        messages.error(request, 'Invalid amount for UPI payment.')
        return redirect('orders:cart')

    token = uuid.uuid4()
    cache.set(
        f"pay:{token}",
        {
            'status': 'pending',
            'cart_data': cart_data,
            'total_amount': total_amount,
            'amount': amount,
            'payment_method': 'upi',
        },
        timeout=15 * 60,
    )

    mark_paid_url = request.build_absolute_uri(
        reverse('orders:upi_mark_paid', kwargs={'token': token})
    )

    status_url = reverse('orders:payment_status', kwargs={'token': token})

    # Generate UPI QR code for payment
    upi_payment_info = None
    try:
        # Create a temporary order ID for QR generation
        temp_order_id = f"temp_{int(token)}"
        upi_payment_info = create_upi_payment_qr(float(amount), temp_order_id)
    except Exception as e:
        messages.warning(request, f'UPI QR generation failed: {str(e)}')
        # Fallback to basic UPI info
        temp_order_id = f"temp_{int(token)}"
        upi_payment_info = get_upi_payment_info(float(amount), temp_order_id)

    context = {
        'cart_data': cart_data,
        'total_amount': total_amount,
        'payment_token': token,
        'upi_mark_paid_url': mark_paid_url,
        'payment_status_url': status_url,
        'upi_payment_info': upi_payment_info,
        'amount': amount,
    }

    return render(request, 'orders/upi_payment.html', context)


def upi_mark_paid_view(request, token):
    payload = cache.get(f"pay:{token}")
    if not payload:
        return render(request, 'orders/upi-expired.html')

    payload['status'] = 'paid'
    cache.set(f"pay:{token}", payload, timeout=15 * 60)

    return render(request, 'orders/upi-paid.html')


def payment_status_view(request, token):
    payload = cache.get(f"pay:{token}")
    if not payload:
        return JsonResponse({'ok': False, 'status': 'expired'})

    return JsonResponse({'ok': True, 'status': payload.get('status', 'pending')})


@login_required
def process_payment_view(request):
    """Process payment and redirect to confirmation"""
    print(f"Processing payment for user: {request.user.username}")
    print(f"Payment method: {request.POST.get('payment_method')}")
    print(f"Cart data: {request.POST.get('cart_data')}")
    
    # Get pending order
    try:
        cart_order = Order.objects.get(
            customer=request.user,
            status=Order.OrderStatus.PENDING
        )
    except Order.DoesNotExist:
        messages.error(request, 'Your cart is empty!')
        return redirect('orders:menu')
    
    # Get payment method from POST or localStorage simulation
    payment_method = request.POST.get('payment_method', 'cod')
    print(f"Payment method received: {payment_method}")

    cart_data_raw = request.POST.get('cart_data', '')
    print(f"Raw cart data: {cart_data_raw}")
    
    if cart_data_raw:
        try:
            cart_data = json.loads(cart_data_raw)
            print(f"Parsed cart data: {cart_data}")
        except json.JSONDecodeError as e:
            print(f"JSON decode error: {e}")
            cart_data = None

        if isinstance(cart_data, list):
            cart_order.items.all().delete()
            for cart_item in cart_data:
                if not isinstance(cart_item, dict):
                    continue

                name = (cart_item.get('name') or '').strip()
                if not name:
                    continue

                try:
                    quantity = int(cart_item.get('quantity', 1))
                except (TypeError, ValueError):
                    quantity = 1

                if quantity < 1:
                    continue

                try:
                    price = Decimal(str(cart_item.get('price', '0')))
                except Exception:
                    price = Decimal('0.00')

                menu_item = MenuItem.objects.filter(name=name).first()
                if not menu_item:
                    menu_item = MenuItem.objects.create(
                        name=name,
                        description=name,
                        price=price if price > 0 else Decimal('0.01'),
                        is_available=True,
                        is_vegetarian=(cart_item.get('category') == 'veg'),
                    )

                OrderItem.objects.create(
                    order=cart_order,
                    menu_item=menu_item,
                    quantity=quantity,
                    price=price if price > 0 else menu_item.price,
                )

            cart_order.calculate_total()
    
    # Get selected table
    table_id = request.session.get('selected_table_id')
    if table_id:
        table = get_object_or_404(Table, id=table_id)
        cart_order.table = table
    
    # Update order with payment info
    cart_order.payment_method = payment_method
    cart_order.special_instructions = request.POST.get('special_instructions', '')
    
    # Confirm order
    cart_order.status = Order.OrderStatus.CONFIRMED
    cart_order.save()
    print(f"Order {cart_order.id} confirmed with status: {cart_order.status}")
    
    request.session['last_confirmed_order_id'] = cart_order.id
    
    # Clear cart from localStorage (will be handled by frontend)
    messages.success(request, f'Order #{cart_order.id} placed successfully!')
    print(f"Redirecting to order confirmation for order {cart_order.id}")
    
    return redirect('orders:order_confirmation')
