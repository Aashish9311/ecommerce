# from django.shortcuts import render

# Create your views here.

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core.paginator import Paginator
from django.db import transaction
from .models import Order, OrderItem
from .forms import ShippingAddressForm
from cart.models import Cart
from cart.decorators import buyer_required

@login_required
@buyer_required
def checkout(request):
    """View for checkout process"""
    cart = get_object_or_404(Cart, user=request.user)
    
    if not cart.items.exists():
        messages.error(request, 'Your cart is empty.')
        return redirect('view_cart')
    
    if request.method == 'POST':
        form = ShippingAddressForm(request.POST)
        
        if form.is_valid():
            with transaction.atomic():
                # Create order
                order = Order.objects.create(
                    user=request.user,
                    total_amount=cart.total,
                    shipping_address=form.get_shipping_address()
                )
                
                # Create order items
                for cart_item in cart.items.all():
                    # Check if product is still in stock
                    product = cart_item.product
                    if product.stock < cart_item.quantity:
                        messages.error(request, f"Sorry, only {product.stock} units of {product.name} are available.")
                        return redirect('view_cart')
                    
                    OrderItem.objects.create(
                        order=order,
                        product=product,
                        quantity=cart_item.quantity,
                        price=product.price
                    )
                    
                    # Update product stock
                    product.stock -= cart_item.quantity
                    product.save()
                
                # Clear the cart
                cart.items.all().delete()
                
                messages.success(request, 'Your order has been placed successfully.')
                return redirect('order_confirmation', order_id=order.id)
    else:
        # Pre-fill form with user information
        initial_data = {}
        if request.user.first_name and request.user.last_name:
            initial_data['full_name'] = f"{request.user.first_name} {request.user.last_name}"
        initial_data['email'] = request.user.email
        initial_data['phone'] = request.user.phone_number
        
        form = ShippingAddressForm(initial=initial_data)
    
    return render(request, 'orders/checkout.html', {'cart': cart, 'form': form})

@login_required
@buyer_required
def order_confirmation(request, order_id):
    """View for order confirmation page"""
    order = get_object_or_404(Order, id=order_id, user=request.user)
    return render(request, 'orders/order_confirmation.html', {'order': order})

@login_required
@buyer_required
def order_history(request):
    """View for displaying order history"""
    orders = Order.objects.filter(user=request.user).order_by('-created_at')
    
    # Pagination
    paginator = Paginator(orders, 10)  # Show 10 orders per page
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    context = {
        'orders': page_obj,
        'is_paginated': page_obj.has_other_pages(),
        'page_obj': page_obj,
    }
    
    return render(request, 'orders/order_history.html', context)

@login_required
@buyer_required
def order_detail(request, order_id):
    """View for displaying order details"""
    order = get_object_or_404(Order, id=order_id, user=request.user)
    return render(request, 'orders/order_detail.html', {'order': order})

@login_required
@buyer_required
def cancel_order_view(request, order_id):
    """View for cancelling an order"""
    order = get_object_or_404(Order, id=order_id, user=request.user)
    
    if order.status != 'pending':
        messages.error(request, 'Only pending orders can be cancelled.')
        return redirect('order_detail', order_id=order.id)
    
    if request.method == 'POST':
        with transaction.atomic():
            order.status = 'cancelled'
            order.save()
            
            # Return items to inventory
            for item in order.items.all():
                product = item.product
                product.stock += item.quantity
                product.save()
            
            messages.success(request, 'Your order has been cancelled successfully.')
        
        return redirect('order_history')
    
    return redirect('order_detail', order_id=order.id)