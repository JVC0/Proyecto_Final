from django.http import JsonResponse
import re
from users.models import Token
from comments.models import Comment


def owner_checker(func):
    def wrapper(request, *args, **kwargs):
        PATTERN = r"^Bearer (?P<token>[0-9a-f]{8}-[0-9a-f]{4}-[0-5][0-9a-f]{3}-[89ab][0-9a-f]{3}-[0-9a-f]{12})$"
        token = request.headers.get("Authorization")
        clean_token = re.fullmatch(PATTERN, token)[1]
        comment = Comment.objects.get(pk=kwargs.get("pk"))
        user = Token.objects.get(key=clean_token)
        if user.user != comment.user:
            return JsonResponse(
                {"error": "User is not the owner of requested comment"}, status=403
            )
        return func(request, *args, **kwargs)

    return wrapper
