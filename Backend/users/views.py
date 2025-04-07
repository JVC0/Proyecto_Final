from .models import Profile
from django.contrib.auth.models import User
from .serializers import ProfileSerializer
from products.serializers import ProductGroupSerializer
from products.models import ProductGroup


def user_profile(request, username):
    user = User.objects.get(username=username)
    profile = Profile.objects.get(user=user)
    serializer = ProfileSerializer(profile, request=request)
    return serializer.json_response()


# def edit_profile(request):
#     pass


# def delete_profile(request):
#     pass


def profile_groups(request, username):
    group_owner = User.objects.get(username=username)
    p_groups = ProductGroup.objects.get(user=group_owner)
    serializer = ProductGroupSerializer(p_groups, request=request)
    return serializer.json_response()


def group_detail(request, username, group_pk):
    p_group = ProductGroup.objects.get(pk=group_pk)
    serializer = ProductGroupSerializer(p_group, request=request)
    return serializer.json_response()
