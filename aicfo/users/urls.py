from django.urls import path
from . import views

urlpatterns = [
    path("hello/", views.user_request)
]