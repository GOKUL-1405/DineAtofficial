from django.contrib.auth.models import AbstractUser
from django.db import models


class CustomUser(AbstractUser):
    """
    Custom User model with role-based access control.
    Supports three user types: Admin, Kitchen Staff, and Customer.
    """
    
    class UserRole(models.TextChoices):
        ADMIN = 'ADMIN', 'Administrator'
        KITCHEN = 'KITCHEN', 'Kitchen Staff'
        CUSTOMER = 'CUSTOMER', 'Customer'
    
    role = models.CharField(
        max_length=10,
        choices=UserRole.choices,
        default=UserRole.CUSTOMER,
        help_text="User role determines access level"
    )
    phone_number = models.CharField(max_length=15, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = 'User'
        verbose_name_plural = 'Users'
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.username} ({self.get_role_display()})"
    
    def is_admin(self):
        """Check if user is an administrator"""
        return self.role == self.UserRole.ADMIN
    
    def is_kitchen_staff(self):
        """Check if user is kitchen staff"""
        return self.role == self.UserRole.KITCHEN
    
    def is_customer(self):
        """Check if user is a customer"""
        return self.role == self.UserRole.CUSTOMER


class CustomerProfile(models.Model):
    """
    Extended customer profile with additional details
    """
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE, related_name='customer_profile')
    
    # Personal Information
    first_name = models.CharField(max_length=50, blank=True)
    last_name = models.CharField(max_length=50, blank=True)
    date_of_birth = models.DateField(null=True, blank=True)
    profile_picture = models.ImageField(upload_to='profile_pics/', null=True, blank=True)
    
    # Contact Information
    address_line1 = models.CharField(max_length=100, blank=True)
    address_line2 = models.CharField(max_length=100, blank=True)
    city = models.CharField(max_length=50, blank=True)
    state = models.CharField(max_length=50, blank=True)
    postal_code = models.CharField(max_length=10, blank=True)
    country = models.CharField(max_length=50, default='India')
    
    # Preferences
    preferred_language = models.CharField(max_length=10, default='en', choices=[
        ('en', 'English'),
        ('ta', 'Tamil'),
        ('hi', 'Hindi'),
    ])
    dietary_preferences = models.CharField(max_length=200, blank=True, help_text="e.g., Vegetarian, Vegan, Gluten-free")
    food_allergies = models.CharField(max_length=200, blank=True)
    
    # Loyalty Program
    loyalty_points = models.IntegerField(default=0)
    total_orders = models.IntegerField(default=0)
    total_spent = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    
    # Notification Preferences
    email_notifications = models.BooleanField(default=True)
    sms_notifications = models.BooleanField(default=False)
    promotional_emails = models.BooleanField(default=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = 'Customer Profile'
        verbose_name_plural = 'Customer Profiles'
    
    def __str__(self):
        return f"{self.user.username}'s Profile"
    
    @property
    def full_name(self):
        """Get full name of the customer"""
        if self.first_name and self.last_name:
            return f"{self.first_name} {self.last_name}"
        elif self.first_name:
            return self.first_name
        else:
            return self.user.username
    
    @property
    def full_address(self):
        """Get formatted full address"""
        address_parts = []
        if self.address_line1:
            address_parts.append(self.address_line1)
        if self.address_line2:
            address_parts.append(self.address_line2)
        if self.city:
            address_parts.append(self.city)
        if self.state:
            address_parts.append(self.state)
        if self.postal_code:
            address_parts.append(self.postal_code)
        if self.country:
            address_parts.append(self.country)
        
        return ', '.join(address_parts)
    
    def add_loyalty_points(self, points):
        """Add loyalty points to customer account"""
        self.loyalty_points += points
        self.save()
    
    def redeem_loyalty_points(self, points):
        """Redeem loyalty points"""
        if self.loyalty_points >= points:
            self.loyalty_points -= points
            self.save()
            return True
        return False
    
    def update_order_stats(self, amount):
        """Update order statistics"""
        self.total_orders += 1
        self.total_spent += amount
        # Add loyalty points (1 point per ₹10 spent)
        points_earned = int(amount // 10)
        self.add_loyalty_points(points_earned)
        self.save()
