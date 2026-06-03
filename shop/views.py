from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.decorators import user_passes_test
from django.contrib import messages
from django.db.models import Q
from .models import Product, Cart, CartItem, Wishlist, WishlistItem, Order, OrderItem, ContactMessage
from .forms import UserRegisterForm, ProductForm, CheckoutForm, ContactForm

# Helper Functions
def get_or_create_cart(request):
    if request.user.is_authenticated:
        cart, created = Cart.objects.get_or_create(user=request.user)
        # Merge session cart if exists
        session_key = request.session.session_key
        if session_key:
            session_cart = Cart.objects.filter(session_key=session_key).first()
            if session_cart and session_cart != cart:
                for item in session_cart.items.all():
                    existing_item = CartItem.objects.filter(cart=cart, product=item.product).first()
                    if existing_item:
                        existing_item.quantity += item.quantity
                        existing_item.save()
                    else:
                        item.cart = cart
                        item.save()
                session_cart.delete()
        return cart
    else:
        if not request.session.session_key:
            request.session.create()
        cart, created = Cart.objects.get_or_create(session_key=request.session.session_key)
        return cart

def get_or_create_wishlist(request):
    if request.user.is_authenticated:
        wishlist, created = Wishlist.objects.get_or_create(user=request.user)
        # Merge session wishlist if exists
        session_key = request.session.session_key
        if session_key:
            session_wishlist = Wishlist.objects.filter(session_key=session_key).first()
            if session_wishlist and session_wishlist != wishlist:
                for item in session_wishlist.items.all():
                    if not WishlistItem.objects.filter(wishlist=wishlist, product=item.product).exists():
                        item.wishlist = wishlist
                        item.save()
                    else:
                        item.delete()
                session_wishlist.delete()
        return wishlist
    else:
        if not request.session.session_key:
            request.session.create()
        wishlist, created = Wishlist.objects.get_or_create(session_key=request.session.session_key)
        return wishlist

# Context Processor for Header (Search, Cart Count, Wishlist Count)
def global_shop_context(request):
    cart = None
    wishlist = None
    cart_count = 0
    wishlist_count = 0
    
    if request.user.is_authenticated:
        cart = Cart.objects.filter(user=request.user).first()
        wishlist = Wishlist.objects.filter(user=request.user).first()
    else:
        session_key = request.session.session_key
        if session_key:
            cart = Cart.objects.filter(session_key=session_key).first()
            wishlist = Wishlist.objects.filter(session_key=session_key).first()
            
    if cart:
        cart_count = sum(item.quantity for item in cart.items.all())
    if wishlist:
        wishlist_count = wishlist.items.count()
        
    return {
        'global_cart_count': cart_count,
        'global_wishlist_count': wishlist_count,
    }

# Views
def indexpage(request):
    featured_products = Product.objects.all()[:4]
    categories = ['Necklaces', 'Rings', 'Pendants', 'Earrings']
    return render(request, 'shop/index.html', {
        'featured_products': featured_products,
        'categories': categories
    })

def catalog(request):
    products = Product.objects.all().order_by('-id')
    query = request.GET.get('q', '')
    category_filter = request.GET.get('category', '')
    price_min = request.GET.get('price_min', '')
    price_max = request.GET.get('price_max', '')
    
    if query:
        products = products.filter(
            Q(name__icontains=query) | Q(description__icontains=query) | Q(category__icontains=query)
        )
    if category_filter:
        products = products.filter(category=category_filter)
    if price_min:
        try:
            products = products.filter(price__gte=float(price_min))
        except ValueError:
            pass
    if price_max:
        try:
            products = products.filter(price__lte=float(price_max))
        except ValueError:
            pass
            
    categories = ['Necklaces', 'Rings', 'Pendants', 'Earrings']
    
    wishlist_product_ids = []
    wishlist = None
    if request.user.is_authenticated:
        wishlist = Wishlist.objects.filter(user=request.user).first()
    else:
        session_key = request.session.session_key
        if session_key:
            wishlist = Wishlist.objects.filter(session_key=session_key).first()
    if wishlist:
        wishlist_product_ids = wishlist.items.values_list('product_id', flat=True)

    return render(request, 'shop/catalog.html', {
        'products': products,
        'categories': categories,
        'query': query,
        'selected_category': category_filter,
        'price_min': price_min,
        'price_max': price_max,
        'wishlist_product_ids': wishlist_product_ids
    })

def product_detail(request, pk):
    product = get_object_or_404(Product, pk=pk)
    
    wishlist_product_ids = []
    wishlist = None
    if request.user.is_authenticated:
        wishlist = Wishlist.objects.filter(user=request.user).first()
    else:
        session_key = request.session.session_key
        if session_key:
            wishlist = Wishlist.objects.filter(session_key=session_key).first()
    if wishlist:
        wishlist_product_ids = wishlist.items.values_list('product_id', flat=True)
        
    related_products = Product.objects.filter(category=product.category).exclude(pk=pk)[:4]
    
    return render(request, 'shop/detail.html', {
        'product': product,
        'related_products': related_products,
        'is_in_wishlist': product.id in wishlist_product_ids
    })

# Authentication
def register_user(request):
    if request.user.is_authenticated:
        return redirect('indexpage')
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(form.cleaned_data['password'])
            user.save()
            login(request, user)
            get_or_create_cart(request)
            get_or_create_wishlist(request)
            messages.success(request, f"Welcome {user.username}! Your account was created successfully.")
            return redirect('indexpage')
    else:
        form = UserRegisterForm()
    return render(request, 'shop/register.html', {'form': form})

def login_user(request):
    if request.user.is_authenticated:
        return redirect('indexpage')
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                get_or_create_cart(request)
                get_or_create_wishlist(request)
                messages.success(request, f"Welcome back, {username}!")
                next_url = request.GET.get('next', 'indexpage')
                return redirect(next_url)
        else:
            messages.error(request, "Invalid username or password.")
    else:
        form = AuthenticationForm()
    return render(request, 'shop/login.html', {'form': form})

def logout_user(request):
    logout(request)
    messages.success(request, "You have been logged out.")
    return redirect('indexpage')

# Cart Views
def cart_detail(request):
    cart = get_or_create_cart(request)
    return render(request, 'shop/cart.html', {'cart': cart})

def cart_add(request, pk):
    product = get_object_or_404(Product, pk=pk)
    quantity = int(request.POST.get('quantity', 1))
    cart = get_or_create_cart(request)
    
    cart_item, created = CartItem.objects.get_or_create(cart=cart, product=product)
    if not created:
        cart_item.quantity += quantity
    else:
        cart_item.quantity = quantity
    cart_item.save()
    
    messages.success(request, f"Added {quantity} x {product.name} to your cart.")
    return redirect('cart_detail')

def cart_remove(request, pk):
    cart = get_or_create_cart(request)
    cart_item = get_object_or_404(CartItem, cart=cart, product_id=pk)
    product_name = cart_item.product.name
    cart_item.delete()
    messages.success(request, f"Removed {product_name} from your cart.")
    return redirect('cart_detail')

def cart_update(request, pk):
    if request.method == 'POST':
        quantity = int(request.POST.get('quantity', 1))
        cart = get_or_create_cart(request)
        cart_item = get_object_or_404(CartItem, cart=cart, product_id=pk)
        if quantity > 0:
            cart_item.quantity = quantity
            cart_item.save()
            messages.success(request, f"Updated quantity for {cart_item.product.name}.")
        else:
            cart_item.delete()
            messages.success(request, f"Removed {cart_item.product.name} from your cart.")
    return redirect('cart_detail')

# Wishlist Views
def wishlist_detail(request):
    wishlist = get_or_create_wishlist(request)
    return render(request, 'shop/wishlist.html', {'wishlist': wishlist})

def wishlist_toggle(request, pk):
    product = get_object_or_404(Product, pk=pk)
    wishlist = get_or_create_wishlist(request)
    
    wishlist_item = WishlistItem.objects.filter(wishlist=wishlist, product=product).first()
    if wishlist_item:
        wishlist_item.delete()
        messages.success(request, f"Removed {product.name} from your wishlist.")
    else:
        WishlistItem.objects.create(wishlist=wishlist, product=product)
        messages.success(request, f"Added {product.name} to your wishlist.")
        
    next_url = request.GET.get('next', 'wishlist_detail')
    return redirect(next_url)

# Checkout & Confirmation
def checkout(request):
    cart = get_or_create_cart(request)
    if cart.items.count() == 0:
        messages.warning(request, "Your cart is empty.")
        return redirect('catalog')
        
    if request.method == 'POST':
        form = CheckoutForm(request.POST)
        if form.is_valid():
            order = form.save(commit=False)
            if request.user.is_authenticated:
                order.user = request.user
            order.total_price = cart.total_price
            order.save()
            
            for item in cart.items.all():
                OrderItem.objects.create(
                    order=order,
                    product=item.product,
                    price=item.product.price,
                    quantity=item.quantity
                )
                item.product.stock = max(0, item.product.stock - item.quantity)
                item.product.save()
                
            cart.items.all().delete()
            
            messages.success(request, "Thank you! Your order has been placed successfully.")
            return redirect('confirmation', order_id=order.id)
    else:
        form = CheckoutForm()
        
    return render(request, 'shop/checkout.html', {
        'cart': cart,
        'form': form
    })

def confirmation(request, order_id):
    order = get_object_or_404(Order, id=order_id)
    return render(request, 'shop/confirmation.html', {'order': order})

# General Pages
def about(request):
    return render(request, 'shop/about.html')

def contact(request):
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Thank you for contacting us! We will get back to you shortly.")
            return redirect('contact')
    else:
        form = ContactForm()
    return render(request, 'shop/contact.html', {'form': form})

# Product CRUD Management
@user_passes_test(lambda u: u.is_superuser, login_url='login')
def manage_products(request):
    products = Product.objects.all().order_by('-id')
    return render(request, 'shop/manage_products.html', {'products': products})

@user_passes_test(lambda u: u.is_superuser, login_url='login')
def add_product(request):
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES)
        if form.is_valid():
            product = form.save()
            messages.success(request, f"Product '{product.name}' was successfully created.")
            return redirect('manage_products')
    else:
        form = ProductForm()
    return render(request, 'shop/product_form.html', {'form': form, 'title': 'Add New Product'})

@user_passes_test(lambda u: u.is_superuser, login_url='login')
def edit_product(request, pk):
    product = get_object_or_404(Product, pk=pk)
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES, instance=product)
        if form.is_valid():
            form.save()
            messages.success(request, f"Product '{product.name}' was successfully updated.")
            return redirect('manage_products')
    else:
        form = ProductForm(instance=product)
    return render(request, 'shop/product_form.html', {'form': form, 'title': f'Edit Product: {product.name}', 'product': product})

@user_passes_test(lambda u: u.is_superuser, login_url='login')
def delete_product(request, pk):
    product = get_object_or_404(Product, pk=pk)
    if request.method == 'POST':
        name = product.name
        product.delete()
        messages.success(request, f"Product '{name}' was deleted.")
        return redirect('manage_products')
    return render(request, 'shop/product_delete.html', {'product': product})
