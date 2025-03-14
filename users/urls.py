from django.urls import path

from . import views

app_name = 'users'

urlpatterns = [
    path('auth/', views.auth, name='auth'),
    # path('api/set-csrf-token/', views.set_csrf_token, name='set_csrf_token'),
    # path('api/login/', views.login_view, name='login'),
    # path('api/logout/', views.logout_view, name='logout'),
    # path('api/user/', views.user, name='user'),
    # path('api/register', views.register, name='register'),
    # path('<username>/', views.user_profile, name='user-profile'),
    path('<username>/edit/', views.edit_profile, name='edit-profile'),
    path('<username>/leave/', views.delete_profile, name='delete-profile'),
    path('<username>/groups/', views.profile_groups, name='profile-groups'),
]