import json

from django.contrib.auth import authenticate
from django.http import JsonResponse

from users.models import Token


def handle_auth_errors(view_func):
    def wrapper(request, *args, **kwargs):
        try:
            if request.body:
                data = json.loads(request.body)
                username = data.get("username")
                password = data.get("password")
                if not username or not password:
                    return JsonResponse(
                        {"message": "Both username and password are required"},
                        status=400,
                    )
                user = authenticate(request, username=username, password=password)
                if user is None:
                    return JsonResponse(
                        {"message": "Invalid username or password"}, status=401
                    )
                try:
                    Token.objects.get(user=user)
                except Token.DoesNotExist:
                    return JsonResponse(
                        {"message": "No token available for this user"}, status=401
                    )
            return view_func(request, *args, **kwargs)
        except json.JSONDecodeError:
            return JsonResponse({"message": "Invalid JSON data"}, status=400)
        except Exception as e:
            return JsonResponse({"message": str(e)}, status=500)

    return wrapper
