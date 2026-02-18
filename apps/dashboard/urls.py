from django.urls import path
from . import views

app_name = 'dashboard'

urlpatterns = [
    path('admin/', views.admin_dashboard_view, name='admin_dashboard'),
    path('kitchen/', views.kitchen_dashboard_view, name='kitchen_dashboard'),
    path('admin/order/<int:order_id>/', views.admin_order_detail_view, name='admin_order_detail'),
    path('admin/order/<int:order_id>/invoice/', views.admin_order_invoice_view, name='admin_order_invoice'),
    path('order/<int:order_id>/update-status/', views.update_order_status, name='update_order_status'),
    path('admin/clear-recent-orders/', views.clear_recent_orders, name='clear_recent_orders'),
    path('admin/stats-api/', views.admin_stats_api, name='admin_stats_api'),
]
