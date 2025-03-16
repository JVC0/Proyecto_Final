from django.http import JsonResponse
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.views.decorators.http import require_http_methods
import json

from django.contrib.auth.models import User
from django.views.decorators.csrf import csrf_exempt


from .models import Token


def get_token(request):
    if request.method == "POST":
        email = request.POST.get("email")
        password = request.POST.get("password")
        user = authenticate(request, email=email, password=password)
        if user is not None:
            login(request, user)
            token = Token.objects.get(user=user)
            return JsonResponse(
                {
                    "token": str(token.key),
                    "user": {
                        "username": user.username,
                        "email": user.email,
                    },
                }
            )
        else:
            return JsonResponse({"error": "Invalid credentials"}, status=400)
    return JsonResponse({"error": "Invalid request method"}, status=405)


# views.py


@csrf_exempt
def register_user(request):
    if request.method == "POST":
        try:
            data = json.loads(request.body)
            email = data.get("email")
            username = data.get("username")
            password = data.get("password")

            # if User.objects.filter(email=email).exists():
            #     return JsonResponse({'error': 'Email already exists'}, status=400)
            # if User.objects.filter(username=username).exists():
            #     return JsonResponse({'error': 'Username already exists'}, status=400)

            user = User.objects.create_user(
                username=username, email=email, password=password
            )
            user.save()

            return JsonResponse({"message": "User registered successfully"})
        except Exception as e:
            return JsonResponse({"error": str(e)}, status=400)
    return JsonResponse({"error": "Invalid request method"}, status=405)


@csrf_exempt  # Disable CSRF protection for this view (temporarily for testing)
def login_view(request):
    if request.method == "POST":
        try:
            data = json.loads(request.body)
            email = data.get("email")  # Use 'email' instead of 'username'
            password = data.get("password")

            # Find the user by email
            try:
                user = User.objects.get(email=email)
            except User.DoesNotExist:
                return JsonResponse(
                    {"error": "User with this email does not exist"}, status=401
                )

            # Authenticate the user
            user = authenticate(request, username=user.username, password=password)

            if user is not None:
                login(request, user)
                return JsonResponse(
                    {
                        "user": {
                            "id": user.id,
                            "username": user.username,
                            "email": user.email,
                        },
                        "token": "your-token-here",  # Add a token if needed
                    }
                )
            else:
                return JsonResponse({"error": "Invalid credentials"}, status=401)
        except json.JSONDecodeError:
            return JsonResponse({"error": "Invalid JSON"}, status=400)
    return JsonResponse({"error": "Invalid request method"}, status=405)


@require_http_methods(["POST"])
def logout_view(request):
    logout(request)
    return JsonResponse({"success": "Logged out"})


# def user_profile(request):
#     pass


# def edit_profile(request):
#     pass


# def delete_profile(request):
#     pass


# def profile_groups(request):
#     pass
