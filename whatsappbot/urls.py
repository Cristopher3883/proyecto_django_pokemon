from django.urls import path
from . import views

urlpatterns = [
    path('whatsapp', views.webhook_verify, name='webhook_verify'),
    path('whatsapp/', views.webhook_message, name='webhook_message'),
]