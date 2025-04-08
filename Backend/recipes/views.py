from .models import Recipe
from .serializers import RecipeSerializer
import json
from django.http import JsonResponse


def recipe_list(request):
    recipes = Recipe.objects.all()
    serializer = RecipeSerializer(recipes, request=request)
    return serializer.json_response()


def recipe_detail(request, recipe_slug):
    recipes = Recipe.objects.get(slug=recipe_slug)
    serializer = RecipeSerializer(recipes, request=request)
    return serializer.json_response()


def add_recipe(request):
    data = json.loads(request.body)
    description = data.get("description")
    name = data.get("name")
    product_group = data.get("product_group")
    user = request.user
    recipe = Recipe.objects.create(
        name=name, description=description, product_group=product_group, user=user
    )
    recipe.save()
    return JsonResponse({"message": "Recipe was added."})


def delete_recipe(request):
    data = json.loads(request.body)
    name = data.get("name")
    recipe = Recipe.objects.get(name=name)
    recipe.delete()
    return JsonResponse({"message": "Recipe was deleted."})


def edit_recipe(request):
    data = json.loads(request.body)
    name = data.get("name")
