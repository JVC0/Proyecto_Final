from django.shortcuts import render
from .models import Comment
from .serializers import CommentSerializer
from recipes.models import Recipe


def comments(request, recipes_slug):
    recipe = Recipe.objects.get(slug=recipes_slug)
    comment = Comment.objects.get(recipe=recipe)
    serializer = CommentSerializer(comment, request=request)
    return serializer.json_response()
