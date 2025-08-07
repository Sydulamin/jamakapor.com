from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
# Create your views here.

def login_view(request):
    return render(request, 'login/login-registration.html')


def logout_view(request):
    logout(request)
    return redirect('login')  # Redirect to login page after logout