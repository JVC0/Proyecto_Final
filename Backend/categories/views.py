from .models import Category
from .serializers import CategorySerializer
from .decorators import check_method


@check_method("GET")
def category_list(request):
    categories = Category.objects.all()
    serializer = CategorySerializer(categories, request=request)
    return serializer.json_response()


@check_method("GET")
def category_detail(category_slug, request):
    category = Category.objects.get(slug=category_slug)
    serializer = CategorySerializer(category, request=request)
    return serializer.json_response()
