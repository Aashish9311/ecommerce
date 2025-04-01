# from django.shortcuts import render

# Create your views here.

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Cart, CartItem
from products.models import Product
from orders.models import Order
from .decorators import buyer_required

@login_required
@buyer_required
def buyer_dashboard(request):
    """Dashboard for buyers"""
    # Get or create cart
    cart, created = Cart.objects.get_or_create(user=request.user)
    
    # Get recent orders
    recent_orders = Order.objects.filter(user=request.user).order_by('-created_at')[:5]
    
    # Get recommended products (simple implementation - just get some random products)
    recommended_products = Product.objects.all().order_by('?')[:4]
    
    context = {
        'cart_items_count': cart.items.count(),
        'orders_count': Order.objects.filter(user=request.user).count(),
        'recent_orders': recent_orders,
        'recommended_products': recommended_products,
    }
    
    return render(request, 'cart/buyer_dashboard.html', context)

@login_required
@buyer_required
def view_cart(request):
    """View for displaying the user's cart"""
    cart, created = Cart.objects.get_or_create(user=request.user)
    return render(request, 'cart/view_cart.html', {'cart': cart})

@login_required
@buyer_required
def add_to_cart(request, product_id):
    """View for adding a product to the cart"""
    product = get_object_or_404(Product, id=product_id)
    
    # Check if product is in stock
    if product.stock <= 0:
        messages.error(request, f"{product.name} is out of stock.")
        return redirect('product_detail', pk=product_id)
    
    cart, created = Cart.objects.get_or_create(user=request.user)
    
    # Get quantity from form if provided
    quantity = int(request.POST.get('quantity', 1))
    
    # Check if quantity is valid
    if quantity <= 0:
        messages.error(request, "Quantity must be greater than zero.")
        return redirect('product_detail', pk=product_id)
    
    if quantity > product.stock:
        messages.error(request, f"Only {product.stock} units of {product.name} are available.")
        return redirect('product_detail', pk=product_id)
    
    # Check if product is already in cart
    cart_item, item_created = CartItem.objects.get_or_create(cart=cart, product=product)
    
    if not item_created:
        # Update quantity if product already in cart
        cart_item.quantity += quantity
        
        # Check if new quantity exceeds stock
        if cart_item.quantity > product.stock:
            messages.error(request, f"Cannot add more units. Only {product.stock} units of {product.name} are available.")
            return redirect('view_cart')
            
        cart_item.save()
    else:
        # Set quantity for new item
        cart_item.quantity = quantity
        cart_item.save()
    
    messages.success(request, f"{product.name} added to your cart.")
    
    # Redirect to referring page or cart
    next_page = request.POST.get('next', 'view_cart')
    return redirect(next_page)

@login_required
@buyer_required
def update_cart(request, item_id):
    """View for updating the quantity of an item in the cart"""
    cart_item = get_object_or_404(CartItem, id=item_id, cart__user=request.user)
    
    if request.method == 'POST':
        quantity = int(request.POST.get('quantity', 1))
        
        # Check if quantity is valid
        if quantity > 0:
            # Check if quantity exceeds stock
            if quantity > cart_item.product.stock:
                messages.error(request, f"Cannot update quantity. Only {cart_item.product.stock} units of {cart_item.product.name} are available.")
            else:
                cart_item.quantity = quantity
                cart_item.save()
        else:
            # Remove item if quantity is 0 or negative
            cart_item.delete()
    
    return redirect('view_cart')

@login_required
@buyer_required
def remove_from_cart(request, item_id):
    """View for removing an item from the cart"""
    cart_item = get_object_or_404(CartItem, id=item_id, cart__user=request.user)
    cart_item.delete()
    
    messages.success(request, f"{cart_item.product.name} removed from your cart.")
    return redirect('view_cart')