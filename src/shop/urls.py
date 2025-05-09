from django.urls import path
from . import views

urlpatterns = [
    # Home Page
    path('', views.home, name='home'),

    path('products/', views.product_list, name='product_list'),
    path('product/<int:pk>/', views.product_detail, name='product_detail'),
    path('add-to-cart/<int:pk>/', views.add_to_cart, name='add_to_cart'),
    path('cart/', views.cart_view, name='cart'),
    path('deals/', views.deals_view, name='deals'),


    
    path('privacy-policy/', views.privacy_policy, name='privacy_policy'),

    # Authentication URLs
    path('login/', views.login_page, name='login'),
    path('register/', views.register_page, name='register'),
    path('logout/', views.logout_view, name='logout'),
    path('forgot/', views.forgot_password, name='forgot'),
    path('reset-password/<str:token>/', views.reset_password, name='reset_password'),
    path('view_demo_email/', views.view_demo_email, name='view_demo_email'),

    # User-related URLs (Profile, Wishlist, Purchases)
    path('profile/', views.profile_view, name='profile'),
    path('wishlist/', views.wishlist_view, name='wishlist'),
    path('purchases/', views.purchases_view, name='purchases'),
]
