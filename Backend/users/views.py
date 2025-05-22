import json

from django.contrib.auth.models import User
from django.views.decorators.csrf import ensure_csrf_cookie

from products.models import Product, ProductGroup, ProductGroupItem
from products.serializers import ProductGroupSerializer
from shared.decorators import check_method
from shared.serializers import JsonResponse

from .models import Profile
from .serializers import ProfileSerializer


def user_profile(request, username):
    user = User.objects.get(username=username)
    profile = Profile.objects.get(user=user)
    serializer = ProfileSerializer(profile, request=request)
    return serializer.json_response()


def delete_profile(username):
    profile_owner = User.objects.get(username=username)
    profile_owner.delete()
    return JsonResponse({"message": "Usuario eliminado."})


def profile_groups(request, username):
    group_owner = User.objects.get(username=username)
    p_groups = ProductGroup.objects.filter(user=group_owner)
    serializer = ProductGroupSerializer(p_groups, request=request)
    return serializer.json_response()


def group_detail(request, username, group_pk):
    p_group = ProductGroup.objects.get(pk=group_pk)
    serializer = ProductGroupSerializer(p_group, request=request)
    return serializer.json_response()


@check_method("POST")
@ensure_csrf_cookie
def add_groups(request):
    try:
        data = json.loads(request.body)
        name = data.get("name")
        productsIDs = data.get("products")

        productgroup = ProductGroup.objects.create(user=request.user, name=name)

        for productid in productsIDs:
            product = Product.objects.get(id=productid)
            ProductGroupItem.objects.create(productgroup=productgroup, product=product)

        return JsonResponse({"message": "Group created successfully"})
    except Exception as e:
        return JsonResponse({"error": str(e)}, status=500)
