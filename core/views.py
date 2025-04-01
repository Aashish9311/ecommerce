# from django.shortcuts import render

# Create your views here.

from django.shortcuts import render
from products.models import Product

def home_view(request):
    """View for homepage"""
    # Get featured products (newest products)
    featured_products = Product.objects.all().order_by('-created_at')[:8]
    
    return render(request, 'core/home.html', {'featured_products': featured_products})