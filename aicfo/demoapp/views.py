from django.shortcuts import render
from . import views

# Create your views here.
def demo_dashboard(request):
    return render(request, 'demo_dashboard.html')