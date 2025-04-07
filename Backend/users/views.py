from .models import Profile
from django.contrib.auth.models import User
from .serializers import ProfileSerializer


def user_profile(request, username):
    user = User.objects.get(username=username)
    profile = Profile.objects.get(user=user)
    serializer = ProfileSerializer(profile, request=request)
    return serializer.json_response()


# def edit_profile(request):
#     pass


# def delete_profile(request):
#     pass


# def profile_groups(request):
#     pass
