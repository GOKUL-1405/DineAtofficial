from django.urls import path
from . import views

app_name = 'orders'

urlpatterns = [
    path('menu/', views.menu_view, name='menu'),
    path('cart/', views.cart_view, name='cart'),
    path('cart/add/<int:item_id>/', views.add_to_cart, name='add_to_cart'),
    path('cart/remove/<int:item_id>/', views.remove_from_cart, name='remove_from_cart'),
    path('cart/update/<int:item_id>/', views.update_cart_item, name='update_cart_item'),
    path('payment/', views.payment_view, name='payment'),
    path('payment/upi/<uuid:token>/mark-paid/', views.upi_mark_paid_view, name='upi_mark_paid'),
    path('payment/upi/<uuid:token>/status/', views.payment_status_view, name='payment_status'),
    path('process-payment/', views.process_payment_view, name='process_payment'),
    path('table-selection/', views.table_selection_view, name='table_selection'),
    path('confirmation/', views.order_confirmation_view, name='order_confirmation'),
    path('upi-payment/', views.upi_payment_view, name='upi_payment'),
]
