// ===================================
// ENHANCED DINEAT RESTAURANT SYSTEM
// Professional Error Handling & Validation
// ===================================

// ===================================
// MOBILE NAVIGATION - HAMBURGER MENU
// ===================================
document.addEventListener('DOMContentLoaded', function() {
    // Mobile Menu Toggle
    const hamburger = document.querySelector('.hamburger');
    const navMenu = document.querySelector('.nav-menu');
    
    if (hamburger && navMenu) {
        hamburger.addEventListener('click', function() {
            hamburger.classList.toggle('active');
            navMenu.classList.toggle('active');
        });
        
        // Close mobile menu when clicking on a link
        document.querySelectorAll('.nav-link').forEach(link => {
            link.addEventListener('click', function() {
                hamburger.classList.remove('active');
                navMenu.classList.remove('active');
            });
        });
        
        // Close mobile menu when clicking outside
        document.addEventListener('click', function(event) {
            if (!hamburger.contains(event.target) && !navMenu.contains(event.target)) {
                hamburger.classList.remove('active');
                navMenu.classList.remove('active');
            }
        });
    }
});

// ===================================
// LANGUAGE MANAGEMENT
// ===================================
function switchLanguage(lang) {
    try {
        if (!['en', 'ta'].includes(lang)) {
            throw new Error('Invalid language selection');
        }

        localStorage.setItem('selectedLanguage', lang);

        // Update active language button
        document.querySelectorAll('.lang-btn').forEach(btn => {
            btn.classList.remove('active');
        });

        const langBtn = document.getElementById(`lang-${lang}`);
        if (langBtn) {
            langBtn.classList.add('active');
        }

        // Add Tamil font class if Tamil is selected
        if (lang === 'ta') {
            document.body.classList.add('ta-text');
        } else {
            document.body.classList.remove('ta-text');
        }

        showNotification(`Language switched to ${lang === 'ta' ? 'Tamil' : 'English'}`, 'success');
    } catch (error) {
        showNotification('Error switching language', 'error');
        console.error('Language switch error:', error);
    }
}

// ===================================
// NAVIGATION & UI
// ===================================
document.addEventListener('DOMContentLoaded', function () {
    try {
        // Initialize language
        const savedLanguage = localStorage.getItem('selectedLanguage') || 'en';
        const langBtn = document.getElementById(`lang-${savedLanguage}`);
        if (langBtn) {
            langBtn.classList.add('active');
        }

        if (savedLanguage === 'ta') {
            document.body.classList.add('ta-text');
        }

        // Initialize hamburger menu
        const hamburger = document.querySelector('.hamburger');
        const navMenu = document.querySelector('.nav-menu');

        if (hamburger && navMenu) {
            hamburger.addEventListener('click', () => {
                hamburger.classList.toggle('active');
                navMenu.classList.toggle('active');
            });

            // Close menu when clicking nav links
            document.querySelectorAll('.nav-link').forEach(link => {
                link.addEventListener('click', () => {
                    hamburger.classList.remove('active');
                    navMenu.classList.remove('active');
                });
            });
        }

        // Check user access and redirect if needed
        checkUserAccess();

        // Update cart on page load
        updateCart();

        // Add smooth scroll behavior
        document.documentElement.style.scrollBehavior = 'smooth';

    } catch (error) {
        console.error('Initialization error:', error);
    }
});

// ===================================
// CART MANAGEMENT
// ===================================
let cart = JSON.parse(localStorage.getItem('cart')) || [];

function addToCart(item) {
    try {
        if (!item || !item.id || !item.name || !item.price) {
            throw new Error('Invalid item data');
        }

        const existingItem = cart.find(cartItem => cartItem.id === item.id);

        if (existingItem) {
            existingItem.quantity += 1;
            showNotification(`${item.name} quantity increased!`, 'success');
        } else {
            cart.push({ ...item, quantity: 1 });
            showNotification(`${item.name} added to cart!`, 'success');
        }

        saveCart();
        updateCart();
    } catch (error) {
        showNotification('Error adding item to cart', 'error');
        console.error('Add to cart error:', error);
    }
}

function removeFromCart(itemId) {
    try {
        const item = cart.find(item => item.id === itemId);
        cart = cart.filter(item => item.id !== itemId);

        saveCart();
        updateCart();

        if (item) {
            showNotification(`${item.name} removed from cart!`, 'success');
        }
    } catch (error) {
        showNotification('Error removing item from cart', 'error');
        console.error('Remove from cart error:', error);
    }
}

function updateCartQuantity(itemId, newQuantity) {
    try {
        const item = cart.find(item => item.id === itemId);

        if (!item) {
            throw new Error('Item not found in cart');
        }

        if (newQuantity <= 0) {
            removeFromCart(itemId);
            return;
        }

        item.quantity = parseInt(newQuantity);
        saveCart();
        updateCart();

    } catch (error) {
        showNotification('Error updating quantity', 'error');
        console.error('Update quantity error:', error);
    }
}

function updateCart() {
    try {
        const cartCount = document.getElementById('cart-count');
        const cartItems = document.getElementById('cart-items');
        const cartTotal = document.getElementById('cart-total');

        // Update cart count
        if (cartCount) {
            const totalItems = cart.reduce((total, item) => total + item.quantity, 0);
            cartCount.textContent = totalItems;
            cartCount.style.display = totalItems > 0 ? 'inline-block' : 'none';
        }

        // Update cart items display
        if (cartItems) {
            cartItems.innerHTML = '';

            if (cart.length === 0) {
                cartItems.innerHTML = '<p class="empty-cart">Your cart is empty</p>';
            } else {
                cart.forEach(item => {
                    const cartItem = document.createElement('div');
                    cartItem.className = 'cart-item';
                    cartItem.innerHTML = `
                        <div class="cart-item-info">
                            <h4>${escapeHtml(item.name)}</h4>
                            <p class="cart-item-price">₹${item.price.toFixed(2)}</p>
                        </div>
                        <div class="cart-item-controls">
                            <button class="btn-quantity" onclick="updateCartQuantity('${item.id}', ${item.quantity - 1})">-</button>
                            <span class="quantity">${item.quantity}</span>
                            <button class="btn-quantity" onclick="updateCartQuantity('${item.id}', ${item.quantity + 1})">+</button>
                        </div>
                    `;
                    cartItems.appendChild(cartItem);
                });
            }
        }

        // Update cart total
        if (cartTotal) {
            const total = cart.reduce((sum, item) => sum + (item.price * item.quantity), 0);
            cartTotal.textContent = `Total: ₹${total.toFixed(2)}`;
        }

    } catch (error) {
        console.error('Update cart error:', error);
    }
}

function saveCart() {
    try {
        localStorage.setItem('cart', JSON.stringify(cart));
    } catch (error) {
        showNotification('Error saving cart', 'error');
        console.error('Save cart error:', error);
    }
}

function clearCart() {
    cart = [];
    saveCart();
    updateCart();
    showNotification('Cart cleared!', 'success');
}

// ===================================
// MENU FILTERING
// ===================================
function filterMenu(category) {
    try {
        const menuItems = document.querySelectorAll('.menu-item');
        const categoryBtns = document.querySelectorAll('.category-btn');

        // Update active button
        categoryBtns.forEach(btn => btn.classList.remove('active'));
        event.target.classList.add('active');

        // Filter items
        menuItems.forEach(item => {
            if (category === 'all' || item.dataset.category === category) {
                item.style.display = 'block';
                item.style.animation = 'fadeIn 0.5s ease';
            } else {
                item.style.display = 'none';
            }
        });

    } catch (error) {
        showNotification('Error filtering menu', 'error');
        console.error('Filter menu error:', error);
    }
}

// ===================================
// ORDER MANAGEMENT
// ===================================
function updateOrderStatus(orderId, status) {
    try {
        if (!orderId || !status) {
            throw new Error('Invalid order ID or status');
        }

        const validStatuses = ['pending', 'preparing', 'ready', 'delivered', 'cancelled'];
        if (!validStatuses.includes(status)) {
            throw new Error('Invalid status');
        }

        showNotification(`Order #${orderId} marked as ${status}`, 'success');

        const orderCard = document.querySelector(`[data-order-id="${orderId}"]`);
        if (orderCard) {
            const statusElement = orderCard.querySelector('.order-status');
            if (statusElement) {
                statusElement.className = `order-status status-${status}`;
                statusElement.textContent = status.charAt(0).toUpperCase() + status.slice(1);
            }
        }

    } catch (error) {
        showNotification('Error updating order status', 'error');
        console.error('Update order status error:', error);
    }
}

// ===================================
// PAYMENT PROCESSING
// ===================================
function processPayment() {
    try {
        const selectedPayment = document.querySelector('input[name="payment"]:checked');

        if (!selectedPayment) {
            showNotification('Please select a payment method', 'error');
            return;
        }

        if (cart.length === 0) {
            showNotification('Your cart is empty', 'error');
            return;
        }

        // Calculate total
        const total = cart.reduce((sum, item) => sum + (item.price * item.quantity), 0);

        if (total <= 0) {
            showNotification('Invalid cart total', 'error');
            return;
        }

        // Store payment details
        localStorage.setItem('paymentMethod', selectedPayment.value);
        localStorage.setItem('totalAmount', total.toFixed(2));
        localStorage.setItem('orderDate', new Date().toISOString());

        // Simulate payment processing
        showNotification('Processing payment...', 'info');

        setTimeout(() => {
            showNotification('Payment successful! Order confirmed.', 'success');

            // Clear cart after successful payment
            clearCart();

            setTimeout(() => {
                window.location.href = '/orders/confirmation/';
            }, 1500);
        }, 2000);

    } catch (error) {
        showNotification('Payment processing failed', 'error');
        console.error('Payment error:', error);
    }
}

// ===================================
// NOTIFICATION SYSTEM
// ===================================
function showNotification(message, type = 'success') {
    try {
        // Remove existing notifications
        const existingNotifications = document.querySelectorAll('.notification');
        existingNotifications.forEach(notif => notif.remove());

        const notification = document.createElement('div');
        notification.className = `notification ${type}`;

        // Add icon based on type
        let icon = '';
        switch (type) {
            case 'success':
                icon = '<i class="fas fa-check-circle"></i>';
                break;
            case 'error':
                icon = '<i class="fas fa-exclamation-circle"></i>';
                break;
            case 'info':
                icon = '<i class="fas fa-info-circle"></i>';
                break;
            case 'warning':
                icon = '<i class="fas fa-exclamation-triangle"></i>';
                break;
        }

        notification.innerHTML = `${icon} <span>${escapeHtml(message)}</span>`;

        notification.style.cssText = `
            position: fixed;
            top: 90px;
            right: 20px;
            padding: 15px 25px;
            background: ${getNotificationColor(type)};
            color: white;
            border-radius: 50px;
            z-index: 10000;
            animation: slideInRight 0.3s ease;
            box-shadow: 0 10px 30px rgba(0,0,0,0.3);
            display: flex;
            align-items: center;
            gap: 10px;
            font-weight: 600;
            backdrop-filter: blur(10px);
        `;

        document.body.appendChild(notification);

        // Auto remove after 3 seconds
        setTimeout(() => {
            notification.style.animation = 'slideOutRight 0.3s ease';
            setTimeout(() => notification.remove(), 300);
        }, 5000);

    } catch (error) {
        console.error('Notification error:', error);
    }
}

function getNotificationColor(type) {
    const colors = {
        success: 'linear-gradient(135deg, #38a169, #2f855a)',
        error: 'linear-gradient(135deg, #e53e3e, #c53030)',
        info: 'linear-gradient(135deg, #3182ce, #2c5282)',
        warning: 'linear-gradient(135deg, #d69e2e, #b7791f)'
    };
    return colors[type] || colors.info;
}

// ===================================
// FORM VALIDATION
// ===================================
function validateForm(formId) {
    try {
        const form = document.getElementById(formId);

        if (!form) {
            throw new Error(`Form with ID "${formId}" not found`);
        }

        const inputs = form.querySelectorAll('input[required], select[required], textarea[required]');
        let isValid = true;

        inputs.forEach(input => {
            // Remove previous error states
            input.classList.remove('error');

            if (!input.value.trim()) {
                input.classList.add('error');
                showNotification(`${input.placeholder || input.name || 'Field'} is required`, 'error');
                input.focus();
                isValid = false;
                return;
            }

            // Email validation
            if (input.type === 'email' && !isValidEmail(input.value)) {
                input.classList.add('error');
                showNotification('Please enter a valid email address', 'error');
                input.focus();
                isValid = false;
                return;
            }

            // Phone validation
            if (input.type === 'tel' && !isValidPhone(input.value)) {
                input.classList.add('error');
                showNotification('Please enter a valid phone number', 'error');
                input.focus();
                isValid = false;
                return;
            }
        });

        return isValid;

    } catch (error) {
        showNotification('Form validation error', 'error');
        console.error('Validation error:', error);
        return false;
    }
}

function isValidEmail(email) {
    const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
    return emailRegex.test(email);
}

function isValidPhone(phone) {
    const phoneRegex = /^[0-9]{10}$/;
    return phoneRegex.test(phone.replace(/[\s\-\(\)]/g, ''));
}

// ===================================
// LOGIN HANDLER
// ===================================
function handleLogin(userType) {
    try {
        // Validate user type
        const validUserTypes = ['customer', 'kitchen', 'admin'];
        if (!validUserTypes.includes(userType)) {
            throw new Error('Invalid user type');
        }

        // Get correct form ID based on user type
        let formId;
        switch (userType) {
            case 'customer':
                formId = 'customerLoginForm';
                break;
            case 'kitchen':
                formId = 'kitchen-login-form';
                break;
            case 'admin':
                formId = 'admin-login-form';
                break;
        }

        // Get form element
        const form = document.getElementById(formId);
        if (!form) {
            throw new Error(`Form not found: ${formId}`);
        }

        // Get form inputs
        const inputs = form.querySelectorAll('input[required]');
        for (let input of inputs) {
            if (!input.value.trim()) {
                showNotification(`${input.placeholder || input.name} is required`, 'error');
                input.focus();
                input.classList.add('error');
                return;
            }
        }

        // Simulate login process
        showNotification('Logging in...', 'info');

        setTimeout(() => {
            localStorage.setItem('userType', userType);
            localStorage.setItem('isLoggedIn', 'true');
            localStorage.setItem('loginTime', new Date().toISOString());

            showNotification('Login successful!', 'success');

            // Redirect based on user type
            const redirectPages = {
                'customer': 'table-selection.html',
                'kitchen': 'kitchen-dashboard.html',
                'admin': 'admin-dashboard.html'
            };

            setTimeout(() => {
                window.location.href = redirectPages[userType];
            }, 1000);
        }, 1500);

    } catch (error) {
        showNotification('Login failed. Please try again.', 'error');
        console.error('Login error:', error);
    }
}

// ===================================
// TABLE SELECTION
// ===================================
function selectTable(tableNumber) {
    try {
        if (!tableNumber || tableNumber < 1) {
            throw new Error('Invalid table number');
        }

        // Store selected table
        localStorage.setItem('selectedTable', tableNumber.toString());
        localStorage.setItem('tableSelectionTime', new Date().toISOString());

        showNotification(`Table ${tableNumber} selected successfully!`, 'success');

        // Redirect to menu page after a short delay
        setTimeout(() => {
            window.location.href = 'menu.html';
        }, 1000);

    } catch (error) {
        showNotification('Error selecting table', 'error');
        console.error('Table selection error:', error);
    }
}

// ===================================
// USER ACCESS CONTROL
// ===================================
function checkUserAccess() {
    try {
        const isLoggedIn = localStorage.getItem('isLoggedIn');
        const userType = localStorage.getItem('userType');
        const currentPage = window.location.pathname.split('/').pop();

        // If logged in user tries to access wrong dashboard
        if (isLoggedIn) {
            if (currentPage === 'kitchen-dashboard.html' && userType !== 'kitchen') {
                window.location.href = userType === 'admin' ? 'admin-dashboard.html' : 'table-selection.html';
                return false;
            }

            if (currentPage === 'admin-dashboard.html' && userType !== 'admin') {
                window.location.href = userType === 'kitchen' ? 'kitchen-dashboard.html' : 'table-selection.html';
                return false;
            }
        }

        return true;

    } catch (error) {
        console.error('Access check error:', error);
        return true;
    }
}

// ===================================
// LOGOUT HANDLER
// ===================================
function logout() {
    try {
        // Clear all user data
        localStorage.removeItem('userType');
        localStorage.removeItem('isLoggedIn');
        localStorage.removeItem('selectedTable');
        localStorage.removeItem('loginTime');
        localStorage.removeItem('tableSelectionTime');

        showNotification('Logged out successfully', 'success');

        setTimeout(() => {
            window.location.href = 'index.html';
        }, 1000);

    } catch (error) {
        showNotification('Error logging out', 'error');
        console.error('Logout error:', error);
    }
}

// ===================================
// RATING SYSTEM
// ===================================
function submitRating(dishId) {
    try {
        if (!dishId) {
            throw new Error('Invalid dish ID');
        }

        const rating = document.querySelector(`input[name="rating-${dishId}"]:checked`);
        const reviewElement = document.getElementById(`review-${dishId}`);
        const review = reviewElement ? reviewElement.value : '';

        if (!rating) {
            showNotification('Please select a rating', 'error');
            return;
        }

        // Store rating
        const ratings = JSON.parse(localStorage.getItem('ratings') || '{}');
        ratings[dishId] = {
            rating: rating.value,
            review: review,
            timestamp: new Date().toISOString()
        };
        localStorage.setItem('ratings', JSON.stringify(ratings));

        showNotification('Thank you for your review!', 'success');

        // Clear form
        if (rating) rating.checked = false;
        if (reviewElement) reviewElement.value = '';

    } catch (error) {
        showNotification('Error submitting rating', 'error');
        console.error('Rating error:', error);
    }
}

// ===================================
// UTILITY FUNCTIONS
// ===================================
function escapeHtml(text) {
    const map = {
        '&': '&amp;',
        '<': '&lt;',
        '>': '&gt;',
        '"': '&quot;',
        "'": '&#039;'
    };
    return text.replace(/[&<>"']/g, m => map[m]);
}

// Add animation styles
const style = document.createElement('style');
style.textContent = `
    @keyframes slideInRight {
        from {
            transform: translateX(100%);
            opacity: 0;
        }
        to {
            transform: translateX(0);
            opacity: 1;
        }
    }
    
    @keyframes slideOutRight {
        from {
            transform: translateX(0);
            opacity: 1;
        }
        to {
            transform: translateX(100%);
            opacity: 0;
        }
    }
    
    @keyframes fadeIn {
        from {
            opacity: 0;
            transform: translateY(20px);
        }
        to {
            opacity: 1;
            transform: translateY(0);
        }
    }
    
    input.error, select.error, textarea.error {
        border-color: #e53e3e !important;
        animation: shake 0.3s ease;
    }
    
    @keyframes shake {
        0%, 100% { transform: translateX(0); }
        25% { transform: translateX(-10px); }
        75% { transform: translateX(10px); }
    }
`;
document.head.appendChild(style);
