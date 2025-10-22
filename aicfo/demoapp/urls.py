from django.urls import path
from . import views

urlpatterns = [
    path('dashboard/', views.demo_dashboard, name='demo_dashboard')
]