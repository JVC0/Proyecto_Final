from django.urls import path

from . import views

app_name = "comments"

urlpatterns = [
    path("add_comment", views.add_comment, name="add_comment"),
    path("edit_comment", views.edit_comment, name="edit_comment"),
    path("delete_comment", views.delete_comment, name="delete_comment"),
]
