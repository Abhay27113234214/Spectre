from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth import authenticate, login, logout
from .models import AppUser
from django.contrib import messages

# Create your views here.
def login_view(request):
    if request.method == 'POST':
        work_email = request.POST.get('work_email')
        password = request.POST.get('password')
        user = authenticate(request, email=work_email, password=password)
        if user:
            login(request, user)
            return redirect('demo_dashboard')
        else:
            messages.error(request, "Invalid Email or password!!")
    return render(request, 'login.html')