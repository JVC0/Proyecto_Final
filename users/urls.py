from django.urls import path

from . import views

app_name = "users"

urlpatterns = [
    path("login/", views.login_view, name="login"),
    path("logout/", views.logout_view, name="logout"),
    path("register/", views.register_user, name="register_user"),
    path("get-token/", views.get_token, name="get_token"),
    # path("<username>/", views.user_profile, name="user-profile"),
    # path("<username>/edit/", views.edit_profile, name="edit-profile"),
    # path("<username>/leave/", views.delete_profile, name="delete-profile"),
    # path("<username>/groups/", views.profile_groups, name="profile-groups"),
]
