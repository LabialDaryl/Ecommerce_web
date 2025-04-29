from django.urls import path
from . import views

urlpatterns = [
    # Home Page
    path('', views.home, name='home'),
    
    # Authentication URLs
    path('login/', views.login_page, name='login'),
    path('register/', views.register_page, name='register'),
    path('logout/', views.logout_view, name='logout'),
    
    # User-related URLs (Profile, Wishlist, Purchases)
    path('profile/', views.profile_view, name='profile'),
    path('wishlist/', views.wishlist_view, name='wishlist'),
    path('purchases/', views.purchases_view, name='purchases'),
]
