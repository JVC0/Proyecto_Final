from .models import Profile
from django.contrib.auth.models import User
from .serializers import ProfileSerializer
from products.serializers import ProductGroupSerializer
from products.models import ProductGroup
from shared.serializers import JsonResponse
from shared.decorators import object_exists

def user_profile(request, username):
    user = User.objects.get(username=username)
    profile = Profile.objects.get(user=user)
    serializer = ProfileSerializer(profile, request=request)
    return serializer.json_response()


# def edit_profile(request):
#     pass


def delete_profile(request, username):
    profile_owner = User.objects.get(username=username)
    profile_owner.delete()
    return JsonResponse({"message": "Usuario eliminado."})


def profile_groups(request, username):
    group_owner = User.objects.get(username=username)
    p_groups = ProductGroup.objects.get(user=group_owner)
    serializer = ProductGroupSerializer(p_groups, request=request)
    return serializer.json_response()

@object_exists(ProductGroup, "pk")
def group_detail(request, username, pk):
    p_group = ProductGroup.objects.get(pk=pk)
    serializer = ProductGroupSerializer(p_group, request=request)
    return serializer.json_response()
