from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied

def home(request):
    """Home page view."""
    return render(request, 'shop/home.html')

def login_page(request):
    """User login page view."""
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(username=username, password=password)
        if user:
            login(request, user)  # Create session
            messages.success(request, 'Successfully logged in')
            return redirect('home')
        else:
            messages.error(request, 'Invalid credentials')
            return render(request, 'authentication/login.html')

    return render(request, 'authentication/login.html')

def register_page(request):
    """User registration page view."""
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        confirm_password = request.POST.get('confirm_password')
        email = request.POST.get('email')

        if User.objects.filter(username=username).exists():
            messages.error(request, 'Username already exists')
        elif password != confirm_password:
            messages.error(request, 'Passwords do not match')
        else:
            user = User.objects.create_user(username=username, password=password, email=email)
            login(request, user)  # Auto-login after registration
            messages.success(request, 'Account created successfully')
            return redirect('home')

    return render(request, 'authentication/register.html')

def logout_view(request):
    """Logout view."""
    logout(request)
    messages.success(request, 'Successfully logged out')
    return redirect('login')

@login_required(login_url='login')  # Redirect unauthenticated users to login page
def profile_view(request):
    """User profile page view."""
    if not request.user.is_authenticated:
        raise PermissionDenied
    return render(request, 'profile/my_account.html', {'user': request.user})

@login_required(login_url='login')  # Redirect unauthenticated users to login page
def wishlist_view(request):
    """User's wishlist view."""
    if not request.user.is_authenticated:
        raise PermissionDenied
    # Fetch user's wishlist items here (this is a placeholder)
    wishlist_items = []  # Replace with actual data from your models
    return render(request, 'profile/wishlist.html', {'wishlist_items': wishlist_items})

@login_required(login_url='login')  # Redirect unauthenticated users to login page
def purchases_view(request):
    """User's purchase history view."""
    if not request.user.is_authenticated:
        raise PermissionDenied
    # Fetch user's purchase history here (this is a placeholder)
    purchases = []  # Replace with actual data from your models
    return render(request, 'profile/purchases.html', {'purchases': purchases})
