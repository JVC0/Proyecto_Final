from .models import Product
from .serializers import ProductSerializer


def products_list(request):
    products = Product.objects.all()
    # category_slug = request.GET.get("category")
    # print(category_slug)
    # if category_slug:
    #     products = products.filter(category__slug=category_slug)
    serializer = ProductSerializer(products, request=request)
    return serializer.json_response()


def product_detail(request):
    pass


def product_group(request):
    pass
