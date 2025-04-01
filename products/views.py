# from django.shortcuts import render

# Create your views here.


from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core.paginator import Paginator
from django.db.models import Q
from .models import Product
from .forms import ProductForm
from .decorators import seller_required

def product_list(request):
    """View for listing all products with filtering and pagination"""
    products = Product.objects.all()
    
    # Search functionality
    query = request.GET.get('q')
    if query:
        products = products.filter(
            Q(name__icontains=query) | 
            Q(description__icontains=query)
        )
    
    # Price range filtering
    min_price = request.GET.get('min_price')
    max_price = request.GET.get('max_price')
    if min_price:
        products = products.filter(price__gte=min_price)
    if max_price:
        products = products.filter(price__lte=max_price)
    
    # Sorting
    sort = request.GET.get('sort', '-created_at')  # Default: newest first
    products = products.order_by(sort)
    
    # Pagination
    paginator = Paginator(products, 12)  # Show 12 products per page
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    context = {
        'products': page_obj,
        'is_paginated': page_obj.has_other_pages(),
        'page_obj': page_obj,
    }
    
    return render(request, 'products/product_list.html', context)

def product_detail(request, pk):
    """View for displaying product details"""
    product = get_object_or_404(Product, pk=pk)
    return render(request, 'products/product_detail.html', {'product': product})

@login_required
@seller_required
def seller_dashboard(request):
    """Dashboard for sellers to manage their products"""
    products = Product.objects.filter(seller=request.user)
    
    # Calculate total sales and pending orders (placeholder for now)
    total_sales = 0
    pending_orders = 0
    
    context = {
        'products': products,
        'total_sales': total_sales,
        'pending_orders': pending_orders,
    }
    
    return render(request, 'products/seller_dashboard.html', context)

@login_required
@seller_required
def add_product(request):
    """View for adding a new product"""
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES)
        if form.is_valid():
            product = form.save(commit=False)
            product.seller = request.user
            product.save()
            messages.success(request, 'Product added successfully.')
            return redirect('seller_dashboard')
    else:
        form = ProductForm()
    
    return render(request, 'products/product_form.html', {'form': form})

@login_required
@seller_required
def edit_product(request, pk):
    """View for editing an existing product"""
    product = get_object_or_404(Product, pk=pk, seller=request.user)
    
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES, instance=product)
        if form.is_valid():
            form.save()
            messages.success(request, 'Product updated successfully.')
            return redirect('seller_dashboard')
    else:
        form = ProductForm(instance=product)
    
    return render(request, 'products/product_form.html', {'form': form, 'product': product})

@login_required
@seller_required
def delete_product(request, pk):
    """View for deleting a product"""
    product = get_object_or_404(Product, pk=pk, seller=request.user)
    
    if request.method == 'POST':
        product.delete()
        messages.success(request, 'Product deleted successfully.')
        return redirect('seller_dashboard')
    
    return render(request, 'products/delete_product.html', {'product': product})