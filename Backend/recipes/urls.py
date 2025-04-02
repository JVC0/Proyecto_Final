from django.urls import path

from . import views

app_name = "recipes"

urlpatterns = [
    path("", views.recipe_list, name="recipe-list"),
    path("add/", views.add_recipe, name="add-recipe"),
    path("delete/", views.delete_recipe, name="del-recipe"),
    path("edit/", views.edit_recipe, name="edit-recipe"),
    path("<slug:recipe_slug>/", views.recipe_detail, name="recipe-detail"),
]
