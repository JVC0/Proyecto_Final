from django.urls import path

from . import views

app_name = "products"

urlpatterns = [
    path("", views.products_list, name="products-list"),
    # path('products/<product_slug>/', views.product_detail, name='product-detail'),
]
