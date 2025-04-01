from django.urls import path
from . import views

urlpatterns = [
    path('seller/dashboard/', views.seller_dashboard, name='seller_dashboard'),
    path('seller/add/', views.add_product, name='add_product'),
    path('seller/edit/<int:pk>/', views.edit_product, name='edit_product'),
    path('seller/delete/<int:pk>/', views.delete_product, name='delete_product'),
    path('', views.product_list, name='product_list'),
    path('<int:pk>/', views.product_detail, name='product_detail'),
]