# Import necessary modules and models

from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User  # Import User for authentication logic
from .models import Professor, Admin

# Define a view function for the home page
def home(request):
    return render(request, 'home.html')

# Define a view function for the login page
def login_page(request):
    if request.method == "POST":
        username = request.POST.get('username').strip()
        password = request.POST.get('password')

        # Custom validation for empty fields
        if not username or not password:
            messages.error(request, "Username and password are required.")
            return redirect('/login/')
        
        # Authenticate the user with the username and password
        user = authenticate(username=username, password=password)

        if user is None:
            messages.error(request, "Invalid username or password.")
            return redirect('/login/')

        if not user.is_active:
            messages.error(request, "Your account is inactive. Please contact support.")
            return redirect('/login/')

        # Check if the user is an admin
        if Admin.objects.filter(email=user.email).exists():
            login(request, user)
            return redirect('/custom-admin-dashboard/')  # to be replaced with our custom admin dashboard URL

        # Check if the user is a professor
        elif Professor.objects.filter(email=user.email).exists():
            login(request, user)
            return redirect('/custom-professor-dashboard/')  # to be replaced with our custom professor dashboard URL

        # Deny access for users who are neither admin nor professor
        else:
            messages.error(request, "Access Denied. You do not have the required permissions.")
            return redirect('/login/')

    return render(request, 'login.html')

# Define custom error handlers
def custom_404(request, exception):
    return render(request, 'custom_404.html', status=404)

def custom_500(request):
    return render(request, 'custom_500.html', status=500)
