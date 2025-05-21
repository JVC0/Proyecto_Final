import json
import re

from django.http import JsonResponse

from users.models import Token


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
            return JsonResponse({"message": "Invalid authentication token"}, status=400)
        try:
            Token.objects.get(key=clean_token["token"])
        except Token.DoesNotExist:
            return JsonResponse(
                {"message": "Unregistered authentication token"}, status=401
            )
        return func(request, *args, **kwargs)

    return wrapper


def invalid_json_body(*required_fields):
    def decorator(func):
        def wrapper(request, *args, **kwargs):
            try:
                data = json.loads(request.body)
            except json.JSONDecodeError:
                return JsonResponse({"error": "Invalid JSON data"}, status=400)
            missing_fields = [field for field in required_fields if field not in data]
            if missing_fields:
                return JsonResponse(
                    {"error": f"Missing required fields: {', '.join(missing_fields)}"},
                    status=400,
                )
            return func(request, *args, **kwargs)

        return wrapper

    return decorator
