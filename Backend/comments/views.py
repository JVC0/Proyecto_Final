from .models import Comment
import json
from django.http import JsonResponse


def add_comment(request):
    data = json.loads(request.body)
    description = data.get("description")
    recipe = data.get("recipe")
    user = request.user
    comment = Comment.objects.create(description=description, recipe=recipe, user=user)
    comment.save()
    return JsonResponse({"message": "Comment was added."})


def delete_comment(request):
    data = json.loads(request.body)  # Pasar id en el front para eliminar comment
    id = data.get("id")
    recipe = Comment.objects.get(pk=id)
    recipe.delete()


def edit_comment(request):
    pass
