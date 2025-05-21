from django.urls import path

from . import views

app_name = "accounts"

urlpatterns = [
    path("login/", views.user_login, name="login"),
    path("logout/", views.user_logout, name="logout"),
    path("register/", views.user_register, name="register"),
    path("verify-email/<token>", views.verify_email, name="verify-email"),
    path(
        "resend-verification/",
        views.resend_verification_email,
        name="resend-verification",
    ),
]
