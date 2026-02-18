from django.urls import path
from . import views
from . import views_chatbot

app_name = 'main'

urlpatterns = [
    path('', views.index_view, name='index'),
    path('about/', views.about_view, name='about'),
    path('contact/', views.contact_view, name='contact'),
    path('help/', views.help_view, name='help'),
    path('payment/', views.payment_view, name='payment'),
    
    # Cookie management URLs
    path('save-preferences/', views.save_preferences, name='save_preferences'),
    path('toggle-theme/', views.toggle_theme, name='toggle_theme'),
    path('cookie-info/', views.get_cookie_info, name='cookie_info'),
    
    # Chatbot URLs
    path('chatbot/query/', views_chatbot.chatbot_query, name='chatbot_query'),
    path('chatbot/status/', views_chatbot.chatbot_status, name='chatbot_status'),
]
