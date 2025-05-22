import json

from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.http import JsonResponse
from django.views.decorators.csrf import ensure_csrf_cookie

from products.models import Product, ProductGroup, ProductGroupItem
from products.serializers import ProductGroupSerializer
from shared.decorators import check_method
from shared.serializers import JsonResponse

from .forms import ProfileForm, UserForm
from .models import Profile
from .serializers import ProfileSerializer


def user_profile(request, username):
    user = User.objects.get(username=username)
    profile = Profile.objects.get(user=user)
    serializer = ProfileSerializer(profile, request=request)
    return serializer.json_response()


@login_required
@check_method("DELETE")
def delete_profile(request, username):
    if request.user.username != username:
        return JsonResponse(
            {"error": "You can only delete your own profile."}, status=403
        )

    try:
        profile_owner = User.objects.get(username=username)
        profile_owner.delete()
        return JsonResponse({"message": "User deleted successfully."})
    except User.DoesNotExist:
        return JsonResponse({"error": "User not found."}, status=404)
    except Exception as e:
        return JsonResponse({"error": str(e)}, status=500)


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


@login_required
def edit_profile(request, username):
    user = User.objects.get(username=username)
    profile = user.profile

    if request.method == "GET":
        data = {
            "first_name": user.first_name,
            "last_name": user.last_name,
            "avatar": request.build_absolute_uri(profile.avatar.url)
            if profile.avatar
            else None,
            "bio": profile.bio,
        }
        return JsonResponse({"status": "success", "data": data})

    elif request.method == "POST":
        user_form = UserForm(request.POST, instance=user)
        profile_form = ProfileForm(request.POST, request.FILES, instance=profile)

        user_valid = user_form.is_valid()
        profile_valid = profile_form.is_valid()

        if user_valid and profile_valid:
            user_form.save()
            profile_form.save()

            updated_data = {
                "first_name": user.first_name,
                "last_name": user.last_name,
                "avatar": request.build_absolute_uri(profile.avatar.url)
                if profile.avatar
                else None,
                "bio": profile.bio,
            }
            return JsonResponse(
                {
                    "status": "success",
                    "message": "Profile updated successfully",
                    "data": updated_data,
                }
            )

        errors = {}
        if not user_valid:
            errors.update(
                {f"user_{field}": error[0] for field, error in user_form.errors.items()}
            )
        if not profile_valid:
            errors.update(
                {
                    f"profile_{field}": error[0]
                    for field, error in profile_form.errors.items()
                }
            )

        return JsonResponse({"status": "error", "errors": errors}, status=400)
