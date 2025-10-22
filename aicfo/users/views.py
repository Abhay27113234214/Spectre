from django.shortcuts import render
from django.http import HttpResponse

# Create your views here.
def user_request(request):
    return HttpResponse("<h1>user you should register!!</h1>")