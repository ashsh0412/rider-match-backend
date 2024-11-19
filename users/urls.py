from django.urls import path
from .views import (
    Me,
    Users,
    ChangePassword,
    LogIn,
    LogOut,
    JWTLogIn,
    PublicUser,
    KakaoLogin,
)
from rest_framework.authtoken.views import obtain_auth_token

urlpatterns = [
    path("", Users.as_view()),
    path("me", Me.as_view()),
    path("change-password", ChangePassword.as_view()),
    path("log-in", LogIn.as_view(), name="login"),
    path("log-out", LogOut.as_view()),
    path("token_login", obtain_auth_token),
    path("jwt_login", JWTLogIn.as_view()),
    path("kakao", KakaoLogin.as_view()),
    path("@<str:username>", PublicUser.as_view()),
]
