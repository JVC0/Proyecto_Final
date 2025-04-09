from django.http import JsonResponse
from users.models import Token
import re


def check_method(method):
    def decorator(func):
        def wrapper(request, *args, **kwargs):
            if request.method != method:
                return JsonResponse({"error": "Method not allowed"}, status=405)
            return func(request, *args, **kwargs)

        return wrapper

    return decorator


def token_checker(func):
    def wrapper(request, *args, **kwargs):
        PATTERN = r"^Bearer (?P<token>[0-9a-f]{8}-[0-9a-f]{4}-[0-5][0-9a-f]{3}-[89ab][0-9a-f]{3}-[0-9a-f]{12})$"
        token = request.headers.get("Authorization")
        clean_token = re.fullmatch(PATTERN, token)
        if not clean_token:
            return JsonResponse({"error": "Invalid authentication token"}, status=400)
        try:
            Token.objects.get(key=clean_token["token"])
        except Token.DoesNotExist:
            return JsonResponse(
                {"error": "Unregistered authentication token"}, status=401
            )
        return func(request, *args, **kwargs)

    return wrapper
