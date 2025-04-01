from django.urls import path

from . import views

app_name = "comments"

urlpatterns = [
    path("<slug:recipes_slug>", views.comments, name="comment-list"),
]
