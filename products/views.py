from django.shortcuts import render
from .models import Product
from .serializers import ProductSerializer
def products_list(request):
    products = Product.objects.all()
    category_slug = request.GET.get('category')
    if category_slug:
        products = products.filter(category__slug=category_slug)#no funciona
    serializer = ProductSerializer(products, request=request)
    return serializer.json_response()

def product_detail(request):
    pass