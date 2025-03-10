app_name = 'products'
from django.urls import path

from . import views

urlpatterns = [
    path('', views.products_list, name='products-list'),
    #path('products/<pk>/', views.product_detail, name='product_detail'),
]