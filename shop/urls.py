from django.urls import path
from . import views

urlpatterns = [
    path('', views.indexpage, name='indexpage'),
    path('products/', views.catalog, name='catalog'),
    path('products/<int:pk>/', views.product_detail, name='product_detail'),
    
    # CRUD Operations
    path('products/manage/', views.manage_products, name='manage_products'),
    path('products/manage/add/', views.add_product, name='add_product'),
    path('products/manage/edit/<int:pk>/', views.edit_product, name='edit_product'),
    path('products/manage/delete/<int:pk>/', views.delete_product, name='delete_product'),
    
    # Authentication
    path('register/', views.register_user, name='register'),
    path('login/', views.login_user, name='login'),
    path('logout/', views.logout_user, name='logout'),
    
    # Cart
    path('cart/', views.cart_detail, name='cart_detail'),
    path('cart/add/<int:pk>/', views.cart_add, name='cart_add'),
    path('cart/remove/<int:pk>/', views.cart_remove, name='cart_remove'),
    path('cart/update/<int:pk>/', views.cart_update, name='cart_update'),
    
    # Wishlist
    path('wishlist/', views.wishlist_detail, name='wishlist_detail'),
    path('wishlist/toggle/<int:pk>/', views.wishlist_toggle, name='wishlist_toggle'),
    
    # Checkout & Confirmation
    path('checkout/', views.checkout, name='checkout'),
    path('confirmation/<int:order_id>/', views.confirmation, name='confirmation'),
    
    # Info Pages
    path('about/', views.about, name='about'),
    path('contact/', views.contact, name='contact'),
]
