from django.http import JsonResponse


def check_method(method):
    def decorator(func):
        def wrapper(request, *args, **kwargs):
            if request.method != method:
                return JsonResponse({"error": "Method not allowed"}, status=405)
            return func(request, *args, **kwargs)

        return wrapper

    return decorator
