from django.shortcuts import render
from .models import Recipe
from .serializers import RecipeSerializer


# Create your views here.
def recipe_list(request):
    recipes = Recipe.objects.all()
    serializer = RecipeSerializer(recipes, request=request)
    return serializer.json_response()


def recipe_detail(request, recipe_slug):
    recipes = Recipe.objects.get(slug=recipe_slug)
    serializer = RecipeSerializer(recipes, request=request)
    return serializer.json_response()
