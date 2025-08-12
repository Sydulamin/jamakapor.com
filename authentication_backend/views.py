from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib import messages
# Create your views here.

def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            messages.success(request, "Login Successful.")
            return redirect('home')
        else:
            messages.error(request, "Invalid username or password.")
    # Render the login page with the registration form
    return render(request, 'login/login-registration.html')

def registration_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password1')
        password1 = request.POST.get('password2')
        if password != password1:
            messages.error(request, "Password not matched.")
        else:
            user = User.objects.create_user( username=username, email=email, password=password)
            user.set_password(password)
            user.backend='django.contrib.auth.backends.ModelBackend'
            user.save()
            login(request, user)
            messages.success(request, "User Created Successfully.")
            return redirect('home')
    return redirect('login')

def logout_view(request):
    logout(request)
    return redirect('login')  # Redirect to login page after logout