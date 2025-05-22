from django.urls import path

from . import views

app_name = "users"

urlpatterns = [
    path("<username>/", views.user_profile, name="user-profile"),
    path("<username>/edit/", views.edit_profile, name="edit-profile"),
    path("<username>/groups/", views.profile_groups, name="profile-groups"),
    path("<username>/delete/", views.delete_profile, name="delete-profile"),
    path("<username>/groups/<group_pk>/", views.group_detail, name="group-detail"),
    path("groups/add/", views.add_groups, name="add-groups"),
]
