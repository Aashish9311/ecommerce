# from django.contrib import admin

# Register your models here.


from django.contrib import admin
from .models import Product

class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'price', 'stock', 'seller', 'created_at')
    list_filter = ('seller', 'created_at')
    search_fields = ('name', 'description')
    readonly_fields = ('created_at', 'updated_at')

admin.site.register(Product, ProductAdmin)