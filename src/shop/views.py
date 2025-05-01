from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied
from django.shortcuts import render, get_object_or_404
from .models import *
from django.core.paginator import Paginator
from django.db.models import Q
from django.utils.crypto import get_random_string
from django.utils.timezone import now, timedelta
from django.urls import reverse
from django.contrib.auth.hashers import make_password


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

    return render(request, 'shop/authentication/login.html')

def register_page(request):
    """User registration page view."""
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        confirm_password = request.POST.get('confirm_password')
        email = request.POST.get('email')

        if User.objects.filter(username=username, email=email, password=password).exists():
            messages.error(request, 'account already exists')
            
        elif password != confirm_password:
            messages.error(request, 'Passwords do not match')
        else:
            user = User.objects.create_user(username=username, password=password, email=email)
            login(request, user)  # Auto-login after registration
            messages.success(request, 'Account created successfully')
            return redirect('home')

    return render(request, 'shop/authentication/register.html')

def logout_view(request):
    """Logout view."""
    logout(request)
    messages.success(request, 'Successfully logged out')
    return redirect('login')

def forgot_password(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        try:
            user = User.objects.get(username=username)

            # Generate token
            token = get_random_string(48)
            expires_at = now() + timedelta(hours=1)

            # Create PasswordReset entry
            PasswordReset.objects.create(user=user, token=token, expires_at=expires_at)

            reset_link = request.build_absolute_uri(
                reverse('reset_password', kwargs={'token': token})
            )

            # Store for demo or email sending
            request.session['demo_emails'] = [{
                'sender': 'support@pawarehauz.com',
                'sender_email': 'support@pawarehauz.com',
                'username': user.username,
                'subject': 'Reset Your Password',
                'body_preview': 'Click the button below to reset your password.',
                'reset_link': reset_link,
                'date': now().strftime('%b %d'),
            }]

            messages.success(request, 'Password reset instructions have been sent to your email.')
            return redirect('view_demo_email')

        except User.DoesNotExist:
            messages.error(request, 'Username not found')

    return render(request, 'shop/authentication/forgot.html')

def reset_password(request, token):
    reset_request = get_object_or_404(PasswordReset, token=token)

    if reset_request.expires_at < now():
        messages.error(request, 'Invalid or expired reset link.')
        return redirect('forgot')  # This should match the name in urls.py

    if request.method == 'POST':
        new_password = request.POST.get('new_password')
        confirm_password = request.POST.get('confirm_password')

        if new_password != confirm_password:
            messages.error(request, 'Passwords do not match.')
            return render(request, 'authentication/reset_password.html', {'token': token})

        user = reset_request.user  # Assuming ForeignKey to User in PasswordReset model
        user.password = make_password(new_password)
        user.save()
        reset_request.delete()

        messages.success(request, 'Your password has been reset successfully.')
        return redirect('login')  # This should match your login URL name

    return render(request, 'shop/authentication/reset_password.html', {'token': token})

def view_demo_email(request):
    demo_emails = request.session.get('demo_emails', [])
    return render(request, 'shop/authentication/gmail_clone.html', {'emails': demo_emails})


@login_required(login_url='login')  # Redirect unauthenticated users to login page
def profile_view(request):
    """User profile page view."""
    if not request.user.is_authenticated:
        raise PermissionDenied
    return render(request, 'shop/profile/my_account.html', {'user': request.user})

@login_required(login_url='login')  # Redirect unauthenticated users to login page
def wishlist_view(request):
    """User's wishlist view."""
    if not request.user.is_authenticated:
        raise PermissionDenied
    # Fetch user's wishlist items here (this is a placeholder)
    wishlist_items = []  # Replace with actual data from your models
    # Example: wishlist_items = request.user.wishlist.all()
    # In a real implementation, you would fetch the wishlist items from the database
    return render(request, 'shop/profile/wishlist.html', {'wishlist_items': wishlist_items})

@login_required(login_url='login')  # Redirect unauthenticated users to login page
def purchases_view(request):
    """User's purchase history view."""
    if not request.user.is_authenticated:
        raise PermissionDenied
    # Fetch user's purchase history here (this is a placeholder)
    purchases = []  # Replace with actual data from your models
    return render(request, 'shop/profile/purchases.html', {'purchases': purchases})

def privacy_policy(request):
    return render(request, 'shop/privacy_policy.html')

    
def product_list(request):
    products = Product.objects.all()
    categories = Category.objects.all()
    
    # Get filter parameters
    category_id = request.GET.get('category')
    search_query = request.GET.get('search')
    sort_by = request.GET.get('sort', 'newest')
    
    # Apply filters
    if category_id:
        products = products.filter(category_id=category_id)
    
    if search_query:
        products = products.filter(
            Q(title__icontains=search_query) |
            Q(description__icontains=search_query)
        )
    
    # Apply sorting
    if sort_by == 'price_low':
        products = products.order_by('price')
    elif sort_by == 'price_high':
        products = products.order_by('-price')
    else:  # newest
        products = products.order_by('-id')
    
    # Pagination
    paginator = Paginator(products, 12)  # Show 12 products per page
    page_number = request.GET.get('page')
    products = paginator.get_page(page_number)
    
    context = {
        'products': products,
        'categories': categories,
        'selected_category': int(category_id) if category_id else None,
    }
    return render(request, 'shop/products.html', context)

def product_detail(request, pk):
    product = get_object_or_404(Product, pk=pk)
    return render(request, 'shop/product_detail.html', {'product': product})

@login_required(login_url='login') 
def add_to_cart(request, pk):
    pass

@login_required(login_url='login')
def cart_view(request):
    """Shopping cart view."""
    # Fetch cart items from the session or database
    cart = request.session.get('cart', {})  # Example: cart stored in session
    cart_items = []
    subtotal = 0

    for product_id, quantity in cart.items():
        product = get_object_or_404(Product, id=product_id)
        cart_items.append({
            'product': product,
            'quantity': quantity,
            'total_price': product.price * quantity
        })
        subtotal += product.price * quantity

    shipping = 5.00  # Example shipping cost
    total = subtotal + shipping

    return render(request, 'shop/cart.html', {
        'cart_items': cart_items,
        'subtotal': subtotal,
        'shipping': shipping,
        'total': total
    })
  
def deals_view(request):
    """Special deals and offers page view."""
    # For now, we'll use placeholder data
    # In a real implementation, you would fetch deals from the database
    featured_deals = [
        {
            'product': {
                'id': 1,
                'name': 'Premium Laptop',
                'description': 'High-performance laptop with latest specs',
                'image': {'url': '/static/shop/images/laptop.jpg'},
            },
            'original_price': 1299.99,
            'discounted_price': 999.99,
            'discount_percentage': 23
        },
        # Add more featured deals as needed
    ]

    daily_deals = [
        {
            'product': {
                'id': 2,
                'name': 'Wireless Headphones',
                'image': {'url': '/static/shop/images/headphones.jpg'},
            },
            'discounted_price': 79.99,
            'time_remaining': '12:34:56'
        },
        # Add more daily deals as needed
    ]

    flash_sale = {
        'product': {
            'id': 3,
            'name': 'Smartphone',
            'image': {'url': '/static/shop/images/phone.jpg'},
        },
        'original_price': 899.99,
        'discounted_price': 699.99,
        'hours': '12',
        'minutes': '34',
        'seconds': '56'
    }

    return render(request, 'shop/deals.html', {
        'featured_deals': featured_deals,
        'daily_deals': daily_deals,
        'flash_sale': flash_sale
    })