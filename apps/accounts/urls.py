from django.urls import path
from . import views

app_name = 'accounts'

urlpatterns = [
    path('login/', views.login_view, name='login'),
    path('login/admin/', views.admin_login_view, name='admin_login'),
    path('login/kitchen/', views.kitchen_login_view, name='kitchen_login'),
    path('login/customer/', views.customer_login_view, name='customer_login'),
    path('signup/customer/', views.customer_signup_view, name='customer_signup'),
    path('logout/', views.logout_view, name='logout'),
    path('profile/', views.profile_view, name='profile'),
    path('profile/edit/', views.edit_profile_view, name='edit_profile'),
    path('orders/', views.order_history_view, name='order_history'),
]
