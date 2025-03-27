from django.urls import path

from . import views

app_name = "categories"

urlpatterns = [
    path("", views.category_list, name="category-list"),
    # path('products/<product_slug>/', views.product_detail, name='product-detail'),
]
