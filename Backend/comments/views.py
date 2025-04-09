from .models import Comment
import json
from django.http import JsonResponse
from .decorators import owner_checker
from shared.decorators import token_checker, check_method


@check_method("POST")
@token_checker
def add_comment(request):
    data = json.loads(request.body)
    description = data.get("description")
    recipe = data.get("recipe")
    user = request.user
    comment = Comment.objects.create(description=description, recipe=recipe, user=user)
    comment.save()
    return JsonResponse({"message": "Comment was added."})


@check_method("POST")
@token_checker
@owner_checker
def delete_comment(request):
    data = json.loads(request.body)  # Pasar id en el front para eliminar comment
    id = data.get("id")
    recipe = Comment.objects.get(pk=id)
    recipe.delete()


@token_checker
@owner_checker
def edit_comment(request):
    pass
