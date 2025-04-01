from django.urls import path

from . import views

app_name = "recipes"

urlpatterns = [
    path("", views.recipe_list, name="recipe-list"),
    path("<slug:recipe_slug>/", views.recipe_detail, name="recipe-detail"),
]
