import json

from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.http import JsonResponse
from django.views.decorators.csrf import ensure_csrf_cookie

from accounts.tasks import send_verification_email
from shared.decorators import check_method, invalid_json_body
from users.models import Profile, Token


@check_method("POST")
@ensure_csrf_cookie
@invalid_json_body("email", "username", "password")
def user_register(request):
    data = json.loads(request.body)
    email = data.get("email")
    username = data.get("username")
    password = data.get("password")
    user = User.objects.create_user(username=username, email=email, password=password)
    token = Token.objects.create(user=user)
    Profile.objects.create(user=user, token=token)
    base_url = request.build_absolute_uri("/")
    send_verification_email.delay(base_url, user)
    return JsonResponse({"message": "User registered successfully"})


@check_method("POST")
def user_login(request):
    data = json.loads(request.body)
    username = data.get("username")
    password = data.get("password")
    user = authenticate(request, username=username, password=password)
    token = Token.objects.get(user=user)
    if user is not None:
        login(request, user)
        return JsonResponse(
            {
                "user": {
                    "id": user.id,
                    "username": user.username,
                    "email": user.email,
                },
                "token": str(token.key),
            }
        )


@check_method("GET")
def user_logout(request):
    logout(request)
    return JsonResponse({"success": "Logged out"})


def verify_email(token):
    if not token:
        return JsonResponse({"error": "Token is required"}, status=400)
    try:
        token_obj = Token.objects.get(key=token)
        token_obj.is_email_verified = True
        token_obj.save()
        return JsonResponse({"success": "Email verified successfully"})
    except Token.DoesNotExist:
        return JsonResponse({"error": "Invalid token"}, status=400)


def resend_verification_email(request):
    base_url = request.build_absolute_uri("/")
    send_verification_email.delay(base_url, request.user)
    return JsonResponse({"success": "Verification email resent"})
